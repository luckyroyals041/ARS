from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import json
import traceback
from datetime import timedelta

from database.mysql_data_handler import get_student_data, get_filtered_student_data, get_students_by_reg_nos, check_database
from reports.generate_pdf_with_styles import generate_pdf_report, generate_pdf_reporting
from reports.generate_excel import generate_excel_report
from reports.academic_reports import register_academic_report_routes
from reports.progress_tracking import register_progress_tracking_routes

# Import blueprints
from auth import auth_bp
from users import users_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key-change-in-production")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)

# Register academic report routes
register_academic_report_routes(app)

# Register progress tracking routes
register_progress_tracking_routes(app)

@app.route('/')
def index():
    """Root endpoint to check if the API is running."""
    if check_database():
        return jsonify({
            "status": "ok", 
            "message": "API is running and database connection is successful",
            "version": "2.0.0"
        })
    else:
        return jsonify({
            "status": "error", 
            "message": "API is running but database connection failed"
        }), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    try:
        branch = request.args.get('branch', '')
        semester = request.args.get('semester', '')
        
        if branch or semester:
            students, _ = get_filtered_student_data(None, semester, branch)
        else:
            students, _, _ = get_student_data()
            
        return jsonify({"data": students})
    except Exception as e:
        print(f"Error in get_students: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e), "data": []}), 500

@app.route('/api/reports/individual/<reg_no>', methods=['GET'])
def get_individual_report(reg_no):
    try:
        include_charts = request.args.get('includeCharts', 'false').lower() == 'true'
        template_style = request.args.get('templateStyle', 'classic')
        
        pdf_path = generate_pdf_report([reg_no], includeCharts=include_charts, template_style=template_style)
        
        if pdf_path:
            return send_file(pdf_path, as_attachment=True, download_name=f"{reg_no}_report.pdf")
        else:
            return jsonify({"error": "Failed to generate PDF"}), 500
    except Exception as e:
        print(f"Error in get_individual_report: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports/preview/<reg_no>', methods=['GET'])
def preview_individual_report(reg_no):
    try:
        include_charts = request.args.get('includeCharts', 'false').lower() == 'true'
        template_style = request.args.get('templateStyle', 'classic')
        
        pdf_path = generate_pdf_report([reg_no], includeCharts=include_charts, template_style=template_style)
        
        if pdf_path:
            # Set Content-Disposition to inline to display in browser
            return send_file(pdf_path, mimetype='application/pdf', 
                            as_attachment=False, 
                            download_name=f"{reg_no}_report.pdf")
        else:
            return jsonify({"error": "Failed to generate PDF"}), 500
    except Exception as e:
        print(f"Error in preview_individual_report: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports/pdf/<pdf_type>', methods=['GET'])
def get_pdf_reports(pdf_type):
    try:
        students_param = request.args.get('students', '')
        include_charts = request.args.get('includeCharts', 'false').lower() == 'true'
        template_style = request.args.get('templateStyle', 'classic')
        
        if not students_param:
            return jsonify({"error": "No students specified"}), 400
            
        students = students_param.split(',')
        
        if pdf_type == 'individual':
            pdf_path = generate_pdf_reporting(students, 'individual', includeCharts=include_charts, template_style=template_style)
            if pdf_path:
                # For individual reports, return the PDF directly
                return send_file(pdf_path, as_attachment=True, 
                                download_name=f"{students[0]}_report.pdf" if len(students) == 1 else "Student_Reports.pdf")
        elif pdf_type == 'combined':
            pdf_path = generate_pdf_reporting(students, 'combined', includeCharts=include_charts, template_style=template_style)
            if pdf_path:
                return send_file(pdf_path, as_attachment=True, download_name="Combined_Student_Report.pdf")
        
        return jsonify({"error": "Failed to generate PDF"}), 500
    except Exception as e:
        print(f"Error in get_pdf_reports: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports/excel', methods=['GET'])
def get_excel_report():
    try:
        students_param = request.args.get('students', '')
        columns_param = request.args.get('columns', '')
        
        if not students_param:
            return jsonify({"error": "No students specified"}), 400
            
        students = students_param.split(',')
        columns = columns_param.split(',') if columns_param else None
        
        excel_path = generate_excel_report(students, columns)
        
        if excel_path:
            return send_file(excel_path, as_attachment=True, download_name="Student_Report.xlsx")
        else:
            return jsonify({"error": "Failed to generate Excel report"}), 500
    except Exception as e:
        print(f"Error in get_excel_report: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    try:
        students, records, summaries = get_student_data()
        
        # Calculate statistics
        total_students = len(students)
        
        # Default values in case of empty data
        avg_cgpa = 0
        at_risk_students = 0
        branches = set()
        
        # Calculate average CGPA if we have data
        if students and summaries:
            student_cgpas = {}
            for summary in summaries:
                reg_no = summary['registered_no']
                if reg_no not in student_cgpas:
                    student_cgpas[reg_no] = {'total_sgpa': 0, 'count': 0}
                
                student_cgpas[reg_no]['total_sgpa'] += summary['sgpa']
                student_cgpas[reg_no]['count'] += 1
            
            if student_cgpas:
                total_cgpa = sum(data['total_sgpa'] / data['count'] for data in student_cgpas.values() if data['count'] > 0)
                avg_cgpa = round(total_cgpa / len(student_cgpas), 2) if student_cgpas else 0
                
                # Count at-risk students (CGPA < 5.0)
                at_risk_students = sum(1 for reg_no, data in student_cgpas.items() 
                                    if data['count'] > 0 and data['total_sgpa'] / data['count'] < 5.0)
        
        # Count branches
        if students:
            branches = set(student['branch'] for student in students)
        
        # Mock reports generated count
        reports_generated = 342
        
        return jsonify({
            "totalStudents": total_students,
            "avgCGPA": avg_cgpa,
            "reportsGenerated": reports_generated,
            "atRiskStudents": at_risk_students,
            "branchCount": len(branches),
            "branches": list(branches)
        })
    except Exception as e:
        print(f"Error in dashboard stats: {e}")
        traceback.print_exc()
        return jsonify({
            "totalStudents": 0,
            "avgCGPA": 0,
            "reportsGenerated": 0,
            "atRiskStudents": 0,
            "branchCount": 0,
            "branches": []
        }), 500

@app.route('/api/dashboard/performance', methods=['GET'])
def get_performance_data():
    try:
        students, records, summaries = get_student_data()
        
        # Default empty response
        empty_response = {
            "labels": [],
            "datasets": [
                {
                    "label": "Average SGPA",
                    "data": [],
                    "borderColor": "#4568dc",
                    "backgroundColor": "rgba(69, 104, 220, 0.2)",
                    "fill": True
                },
                {
                    "label": "Pass Percentage",
                    "data": [],
                    "borderColor": "#b06ab3",
                    "backgroundColor": "rgba(176, 106, 179, 0.2)",
                    "fill": True
                }
            ]
        }
        
        # If no data, return empty response
        if not summaries:
            return jsonify(empty_response)
        
        # Group summaries by semester
        semester_data = {}
        for summary in summaries:
            sem_no = summary['semester_no']
            if sem_no not in semester_data:
                semester_data[sem_no] = {
                    'total_sgpa': 0,
                    'count': 0,
                    'pass_count': 0,
                    'total_subjects': 0,
                    'failed_subjects': 0
                }
            
            semester_data[sem_no]['total_sgpa'] += summary['sgpa']
            semester_data[sem_no]['count'] += 1
            semester_data[sem_no]['total_subjects'] += summary['total_no_of_subjects']
            semester_data[sem_no]['failed_subjects'] += summary['no_of_failed_subjects']
        
        # If no semester data, return empty response
        if not semester_data:
            return jsonify(empty_response)
        
        # Calculate average SGPA and pass percentage for each semester
        labels = []
        sgpa_data = []
        pass_percentage_data = []
        
        for sem_no in sorted(semester_data.keys()):
            data = semester_data[sem_no]
            labels.append(f'Semester {sem_no}')
            
            avg_sgpa = round(data['total_sgpa'] / data['count'], 2) if data['count'] > 0 else 0
            sgpa_data.append(avg_sgpa)
            
            total_subjects = data['total_subjects']
            passed_subjects = total_subjects - data['failed_subjects']
            pass_percentage = round((passed_subjects / total_subjects) * 100, 1) if total_subjects > 0 else 0
            pass_percentage_data.append(pass_percentage)
        
        return jsonify({
            "labels": labels,
            "datasets": [
                {
                    "label": "Average SGPA",
                    "data": sgpa_data,
                    "borderColor": "#4568dc",
                    "backgroundColor": "rgba(69, 104, 220, 0.2)",
                    "fill": True
                },
                {
                    "label": "Pass Percentage",
                    "data": pass_percentage_data,
                    "borderColor": "#b06ab3",
                    "backgroundColor": "rgba(176, 106, 179, 0.2)",
                    "fill": True
                }
            ]
        })
    except Exception as e:
        print(f"Error in performance data: {e}")
        traceback.print_exc()
        return jsonify(empty_response), 500

@app.route('/api/dashboard/branch-distribution', methods=['GET'])
def get_branch_distribution():
    try:
        students, _, _ = get_student_data()
        
        # Default empty response
        empty_response = {
            "labels": [],
            "datasets": [{
                "data": [],
                "backgroundColor": []
            }]
        }
        
        # If no students, return empty response
        if not students:
            return jsonify(empty_response)
        
        # Count students by branch
        branch_counts = {}
        for student in students:
            branch = student['branch']
            if branch not in branch_counts:
                branch_counts[branch] = 0
            branch_counts[branch] += 1
        
        # If no branch counts, return empty response
        if not branch_counts:
            return jsonify(empty_response)
        
        # Prepare data for chart
        labels = list(branch_counts.keys())
        data = list(branch_counts.values())
        
        # Define colors for branches
        colors = [
            '#4568dc', '#b06ab3', '#4caf50', '#ff9800', '#2196f3', '#f44336',
            '#9c27b0', '#673ab7', '#3f51b5', '#009688', '#ffeb3b', '#795548'
        ]
        
        return jsonify({
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": colors[:len(labels)]
            }]
        })
    except Exception as e:
        print(f"Error in branch distribution: {e}")
        traceback.print_exc()
        return jsonify(empty_response), 500

@app.route('/api/dashboard/recent-reports', methods=['GET'])
def get_recent_reports():
    # Mock data - in a real implementation, this would come from a database
    return jsonify([
        {"id": 1, "type": "PDF", "name": "Semester Report", "date": "2023-05-10", "user": "Admin"},
        {"id": 2, "type": "Excel", "name": "Branch Comparison", "date": "2023-05-09", "user": "Admin"},
        {"id": 3, "type": "PDF", "name": "Individual Report", "date": "2023-05-08", "user": "Admin"},
        {"id": 4, "type": "PDF", "name": "Batch Analysis", "date": "2023-05-07", "user": "Admin"},
        {"id": 5, "type": "Excel", "name": "CGPA Summary", "date": "2023-05-06", "user": "Admin"}
    ])

@app.route('/api/dashboard/notifications', methods=['GET'])
def get_notifications():
    # Mock data - in a real implementation, this would come from a database
    return jsonify([
        {
            "id": 1,
            "type": "warning",
            "message": "5 students have CGPA below 5.0",
            "details": "Action required",
            "time": "2 hours ago"
        },
        {
            "id": 2,
            "type": "success",
            "message": "Semester reports generated successfully",
            "details": "System notification",
            "time": "Yesterday"
        },
        {
            "id": 3,
            "type": "info",
            "message": "New academic calendar published",
            "details": "Admin notification",
            "time": "2 days ago"
        }
    ])

if __name__ == '__main__':
    app.run(debug=True)