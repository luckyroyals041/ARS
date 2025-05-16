import os
import traceback
from flask import jsonify, request
from database.mysql_data_handler import get_connection

def register_academic_report_routes(app):
    """Register all academic report routes with the Flask app."""
    
    @app.route('/api/reports/semester-performance/<reg_no>', methods=['GET'])
    def get_semester_performance(reg_no):
        try:
            semester = request.args.get('semester', '')
            academic_year = request.args.get('academic_year', '')
            
            if not semester:
                return jsonify({"error": "Semester parameter is required"}), 400
                
            conn = get_connection()
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
                
            cursor = conn.cursor(dictionary=True)
            
            # Get student data
            cursor.execute("""
                SELECT 
                    registration_number AS registered_no,
                    name,
                    branch,
                    current_semester AS curr_semester
                FROM students
                WHERE registration_number = %s
            """, (reg_no,))
            
            student = cursor.fetchone()
            if not student:
                return jsonify({"error": "Student not found"}), 404
                
            # Get semester records
            cursor.execute("""
                SELECT 
                    g.course_code,
                    c.name AS course_name,
                    c.credits,
                    c.subject_type,
                    c.course_type,
                    g.grade,
                    g.grade_points,
                    g.credits_obtained,
                    g.result
                FROM grades g
                JOIN courses c ON g.course_code = c.code
                WHERE g.registration_number = %s AND c.semester = %s
            """, (reg_no, semester))
            
            semester_records = cursor.fetchall()
            
            # Calculate SGPA
            total_credits = sum(record['credits'] for record in semester_records) if semester_records else 0
            total_grade_points = sum(record['grade_points'] * record['credits'] for record in semester_records) if semester_records else 0
            sgpa = round(total_grade_points / total_credits, 2) if total_credits > 0 else 0
            
            # Get failed subjects
            failed_subjects = [record for record in semester_records if record['result'] == 'FAIL']
            
            # Get class average for comparison
            cursor.execute("""
                SELECT 
                    ca.course_code,
                    ca.average_grade_points,
                    ca.pass_percentage
                FROM class_averages ca
                WHERE ca.branch = %s AND ca.semester = %s AND ca.academic_year = %s
            """, (student['branch'], semester, academic_year))
            
            class_averages = cursor.fetchall()
            
            # Convert to dictionary for easier lookup
            class_avg_dict = {avg['course_code']: avg for avg in class_averages}
            
            # Add class average to each course record
            for record in semester_records:
                course_code = record['course_code']
                if course_code in class_avg_dict:
                    record['class_avg_grade_points'] = class_avg_dict[course_code]['average_grade_points']
                    record['class_pass_percentage'] = class_avg_dict[course_code]['pass_percentage']
                else:
                    record['class_avg_grade_points'] = 0
                    record['class_pass_percentage'] = 0
            
            # Generate recommendations for failed subjects
            recommendations = []
            for subject in failed_subjects:
                recommendations.append({
                    "course_code": subject['course_code'],
                    "course_name": subject['course_name'],
                    "recommendation": f"Focus on improving understanding of {subject['course_name']}. Consider additional tutoring or study groups."
                })
            
            # Prepare data for visualization
            course_names = [record['course_name'] for record in semester_records]
            student_grades = [record['grade_points'] for record in semester_records]
            class_avg_grades = [record.get('class_avg_grade_points', 0) for record in semester_records]
            
            visual_data = {
                "labels": course_names,
                "datasets": [
                    {
                        "label": "Your Grade Points",
                        "data": student_grades,
                        "backgroundColor": "rgba(69, 104, 220, 0.7)",
                        "borderColor": "#4568dc",
                        "borderWidth": 1
                    },
                    {
                        "label": "Class Average",
                        "data": class_avg_grades,
                        "backgroundColor": "rgba(176, 106, 179, 0.7)",
                        "borderColor": "#b06ab3",
                        "borderWidth": 1
                    }
                ]
            }
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "student": student,
                "semester": semester,
                "academicYear": academic_year,
                "records": semester_records,
                "sgpa": sgpa,
                "failedSubjects": failed_subjects,
                "recommendations": recommendations,
                "visualData": visual_data
            })
            
        except Exception as e:
            print(f"Error generating semester performance report: {e}")
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @app.route('/api/reports/cumulative-performance/<reg_no>', methods=['GET'])
    def get_cumulative_performance(reg_no):
        try:
            conn = get_connection()
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
                
            cursor = conn.cursor(dictionary=True)
            
            # Get student data
            cursor.execute("""
                SELECT 
                    registration_number AS registered_no,
                    name,
                    branch,
                    current_semester AS curr_semester
                FROM students
                WHERE registration_number = %s
            """, (reg_no,))
            
            student = cursor.fetchone()
            if not student:
                return jsonify({"error": "Student not found"}), 404
                
            # Get all semester records grouped by semester
            cursor.execute("""
                SELECT 
                    c.semester,
                    g.course_code,
                    c.name AS course_name,
                    c.credits,
                    g.grade,
                    g.grade_points,
                    g.credits_obtained,
                    g.result
                FROM grades g
                JOIN courses c ON g.course_code = c.code
                WHERE g.registration_number = %s
                ORDER BY c.semester
            """, (reg_no,))
            
            all_records = cursor.fetchall()
            
            # Group records by semester
            semester_records = {}
            for record in all_records:
                sem = record['semester']
                if sem not in semester_records:
                    semester_records[sem] = []
                semester_records[sem].append(record)
            
            # Calculate SGPA for each semester
            sgpa_by_semester = {}
            for sem, records in semester_records.items():
                total_credits = sum(record['credits'] for record in records)
                total_grade_points = sum(record['grade_points'] * record['credits'] for record in records)
                sgpa_by_semester[sem] = round(total_grade_points / total_credits, 2) if total_credits > 0 else 0
            
            # Calculate CGPA
            all_credits = sum(record['credits'] for record in all_records)
            all_grade_points = sum(record['grade_points'] * record['credits'] for record in all_records)
            cgpa = round(all_grade_points / all_credits, 2) if all_credits > 0 else 0
            
            # Calculate credit accumulation
            credits_by_semester = {}
            cumulative_credits = 0
            for sem in sorted(semester_records.keys()):
                sem_credits = sum(record['credits'] for record in semester_records[sem])
                cumulative_credits += sem_credits
                credits_by_semester[sem] = {
                    "semester_credits": sem_credits,
                    "cumulative_credits": cumulative_credits
                }
            
            # Track backlogs
            backlogs_by_semester = {}
            for sem, records in semester_records.items():
                backlogs_by_semester[sem] = [
                    {
                        "course_code": record['course_code'],
                        "course_name": record['course_name'],
                        "credits": record['credits']
                    }
                    for record in records if record['result'] == 'FAIL'
                ]
            
            # Calculate total pending backlogs
            all_backlogs = []
            for sem, backlogs in backlogs_by_semester.items():
                all_backlogs.extend(backlogs)
            
            # Estimate graduation timeline
            current_sem = student['curr_semester']
            normal_completion_sem = 8  # Assuming B.Tech is 8 semesters
            backlog_delay_semesters = len(all_backlogs) // 4  # Assuming a student can clear ~4 backlogs per semester
            projected_completion_sem = max(current_sem, normal_completion_sem) + backlog_delay_semesters
            
            # Prepare data for CGPA trend visualization
            semesters = sorted(sgpa_by_semester.keys())
            sgpa_values = [sgpa_by_semester[sem] for sem in semesters]
            
            # Calculate running CGPA
            running_cgpa = []
            total_credits_so_far = 0
            total_grade_points_so_far = 0
            
            for sem in semesters:
                for record in semester_records[sem]:
                    total_credits_so_far += record['credits']
                    total_grade_points_so_far += record['grade_points'] * record['credits']
                
                if total_credits_so_far > 0:
                    running_cgpa.append(round(total_grade_points_so_far / total_credits_so_far, 2))
                else:
                    running_cgpa.append(0)
            
            visual_data = {
                "labels": [f"Semester {sem}" for sem in semesters],
                "datasets": [
                    {
                        "label": "SGPA",
                        "data": sgpa_values,
                        "borderColor": "#4568dc",
                        "backgroundColor": "rgba(69, 104, 220, 0.2)",
                        "fill": False
                    },
                    {
                        "label": "CGPA",
                        "data": running_cgpa,
                        "borderColor": "#b06ab3",
                        "backgroundColor": "rgba(176, 106, 179, 0.2)",
                        "fill": False
                    }
                ]
            }
            
            # Prepare credit accumulation data
            credit_data = {
                "labels": [f"Semester {sem}" for sem in sorted(credits_by_semester.keys())],
                "datasets": [
                    {
                        "label": "Cumulative Credits",
                        "data": [credits_by_semester[sem]["cumulative_credits"] for sem in sorted(credits_by_semester.keys())],
                        "borderColor": "#4caf50",
                        "backgroundColor": "rgba(76, 175, 80, 0.2)",
                        "fill": True
                    }
                ]
            }
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "student": student,
                "cgpa": cgpa,
                "sgpaBySemseter": sgpa_by_semester,
                "creditAccumulation": credits_by_semester,
                "backlogsBySemester": backlogs_by_semester,
                "totalPendingBacklogs": len(all_backlogs),
                "projectedGraduation": {
                    "normalCompletionSemester": normal_completion_sem,
                    "projectedCompletionSemester": projected_completion_sem,
                    "backlogDelaySemesters": backlog_delay_semesters
                },
                "visualData": visual_data,
                "creditData": credit_data
            })
            
        except Exception as e:
            print(f"Error generating cumulative performance report: {e}")
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @app.route('/api/reports/subject-analysis/<reg_no>', methods=['GET'])
    def get_subject_analysis(reg_no):
        try:
            conn = get_connection()
            if not conn:
                return jsonify({"error": "Database connection failed"}), 500
                
            cursor = conn.cursor(dictionary=True)
            
            # Get student data
            cursor.execute("""
                SELECT 
                    registration_number AS registered_no,
                    name,
                    branch,
                    current_semester AS curr_semester
                FROM students
                WHERE registration_number = %s
            """, (reg_no,))
            
            student = cursor.fetchone()
            if not student:
                return jsonify({"error": "Student not found"}), 404
                
            # Get all subject records with categorization
            cursor.execute("""
                SELECT 
                    g.course_code,
                    c.name AS course_name,
                    c.credits,
                    c.subject_type,
                    c.course_type,
                    c.semester,
                    c.department,
                    g.grade,
                    g.grade_points,
                    g.result
                FROM grades g
                JOIN courses c ON g.course_code = c.code
                WHERE g.registration_number = %s
            """, (reg_no,))
            
            all_subjects = cursor.fetchall()
            
            # Group by subject type (core vs elective)
            core_subjects = [subj for subj in all_subjects if subj['subject_type'] == 'core']
            elective_subjects = [subj for subj in all_subjects if subj['subject_type'] == 'elective']
            
            # Group by course type (theory vs lab)
            theory_subjects = [subj for subj in all_subjects if subj['course_type'] == 'theory']
            lab_subjects = [subj for subj in all_subjects if subj['course_type'] == 'lab']
            
            # Group by department
            dept_subjects = {}
            for subj in all_subjects:
                dept = subj['department']
                if dept not in dept_subjects:
                    dept_subjects[dept] = []
                dept_subjects[dept].append(subj)
            
            # Calculate performance metrics
            def calculate_metrics(subjects):
                if not subjects:
                    return {
                        "average_grade_points": 0,
                        "pass_percentage": 100,
                        "total_credits": 0,
                        "credits_obtained": 0
                    }
                    
                total_subjects = len(subjects)
                passed_subjects = sum(1 for s in subjects if s['result'] == 'PASS')
                total_credits = sum(s['credits'] for s in subjects)
                total_grade_points = sum(s['grade_points'] * s['credits'] for s in subjects)
                
                return {
                    "average_grade_points": round(total_grade_points / total_credits, 2) if total_credits > 0 else 0,
                    "pass_percentage": round((passed_subjects / total_subjects) * 100, 1) if total_subjects > 0 else 100,
                    "total_credits": total_credits,
                    "credits_obtained": sum(s['credits'] for s in subjects if s['result'] == 'PASS')
                }
            
            # Calculate metrics for each category
            core_metrics = calculate_metrics(core_subjects)
            elective_metrics = calculate_metrics(elective_subjects)
            theory_metrics = calculate_metrics(theory_subjects)
            lab_metrics = calculate_metrics(lab_subjects)
            
            # Calculate department-wise metrics
            dept_metrics = {dept: calculate_metrics(subjects) for dept, subjects in dept_subjects.items()}
            
            # Identify strengths and weaknesses
            all_grade_points = [subj['grade_points'] for subj in all_subjects]
            avg_grade_points = sum(all_grade_points) / len(all_grade_points) if all_grade_points else 0
            
            strengths = [
                {
                    "course_code": subj['course_code'],
                    "course_name": subj['course_name'],
                    "grade_points": subj['grade_points'],
                    "subject_type": subj['subject_type'],
                    "course_type": subj['course_type'],
                    "department": subj['department']
                }
                for subj in all_subjects if subj['grade_points'] > avg_grade_points + 1
            ]
            
            weaknesses = [
                {
                    "course_code": subj['course_code'],
                    "course_name": subj['course_name'],
                    "grade_points": subj['grade_points'],
                    "subject_type": subj['subject_type'],
                    "course_type": subj['course_type'],
                    "department": subj['department']
                }
                for subj in all_subjects if subj['grade_points'] < avg_grade_points - 1 or subj['result'] == 'FAIL'
            ]
            
            # Prepare visualization data
            subject_type_data = {
                "labels": ["Core", "Elective"],
                "datasets": [
                    {
                        "label": "Average Grade Points",
                        "data": [core_metrics["average_grade_points"], elective_metrics["average_grade_points"]],
                        "backgroundColor": ["rgba(69, 104, 220, 0.7)", "rgba(176, 106, 179, 0.7)"],
                        "borderColor": ["#4568dc", "#b06ab3"],
                        "borderWidth": 1
                    }
                ]
            }
            
            course_type_data = {
                "labels": ["Theory", "Lab"],
                "datasets": [
                    {
                        "label": "Average Grade Points",
                        "data": [theory_metrics["average_grade_points"], lab_metrics["average_grade_points"]],
                        "backgroundColor": ["rgba(76, 175, 80, 0.7)", "rgba(255, 152, 0, 0.7)"],
                        "borderColor": ["#4caf50", "#ff9800"],
                        "borderWidth": 1
                    }
                ]
            }
            
            department_data = {
                "labels": list(dept_metrics.keys()),
                "datasets": [
                    {
                        "label": "Average Grade Points",
                        "data": [metrics["average_grade_points"] for metrics in dept_metrics.values()],
                        "backgroundColor": "rgba(33, 150, 243, 0.7)",
                        "borderColor": "#2196f3",
                        "borderWidth": 1
                    }
                ]
            }
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "student": student,
                "subjectTypeAnalysis": {
                    "core": {
                        "subjects": core_subjects,
                        "metrics": core_metrics
                    },
                    "elective": {
                        "subjects": elective_subjects,
                        "metrics": elective_metrics
                    }
                },
                "courseTypeAnalysis": {
                    "theory": {
                        "subjects": theory_subjects,
                        "metrics": theory_metrics
                    },
                    "lab": {
                        "subjects": lab_subjects,
                        "metrics": lab_metrics
                    }
                },
                "departmentAnalysis": {
                    "departments": dept_subjects,
                    "metrics": dept_metrics
                },
                "strengthsAndWeaknesses": {
                    "strengths": strengths,
                    "weaknesses": weaknesses
                },
                "visualData": {
                    "subjectTypeData": subject_type_data,
                    "courseTypeData": course_type_data,
                    "departmentData": department_data
                }
            })
            
        except Exception as e:
            print(f"Error generating subject analysis report: {e}")
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500