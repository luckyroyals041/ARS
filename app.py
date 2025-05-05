from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
from database.fetch_data import fetch_student_data
from reports.generate_pdf import generate_pdf_report,generate_pdf_reporting
from reports.generate_excel import generate_excel_report
import os

app = Flask(__name__)
CORS(app)


@app.route("/students", methods=["GET"])
def get_students():
    branch_filter = request.args.get("branch")
    semester_filter = request.args.get("curr_semester")

    # Fetch full student data (basic info only for table)
    students, _, _ = fetch_student_data()

    # Apply optional filters
    filtered_students = []
    for s in students:
        if branch_filter and s["branch"] != branch_filter:
            continue
        if semester_filter and str(s["curr_semester"]) != str(semester_filter):
            continue
        filtered_students.append({
            "registered_no": s["registered_no"],
            "name": s["name"],
            "branch": s["branch"],
            "curr_semester": s["curr_semester"]
        })

    return jsonify(filtered_students)


@app.route("/generate-pdf-report", methods=["POST"])
def handle_generate_pdf_report():
    print("genreate pdf api called...")
    
    data = request.get_json()
    selected_students = data.get("selected_students", [])
    generation_type = data.get("generation_type")
    
    if not selected_students or generation_type not in {"individual", "combined"}:
        return jsonify({"error": "Invalid request"}), 400

    output_path = generate_pdf_reporting(selected_students, generation_type)

    if not output_path or not os.path.exists(output_path):
        return jsonify({"error": "PDF generation failed"}), 500

    download_name = (
        "Combined_Student_Report.pdf"
        if generation_type == "combined"
        else "Student_Reports.zip"
    )

    return send_file(
        output_path,
        as_attachment=True,
        download_name=download_name,
        mimetype="application/pdf" if generation_type == "combined" else "application/zip"
    )


@app.route('/generate-excel-report', methods=['POST'])
def handle_generate_excel_report():
    """Generate Excel report"""
    
    data = request.json
    selected_students = data.get('selected_students', [])
    selected_columns = data.get('selected_columns', [])
    
    try:
        # Generate report and get the path
        excel_path = generate_excel_report(selected_students, selected_columns)
        
        if not excel_path:
            return jsonify({"error": "No student data available for the selected filters"}), 400
            
        # Send the file
        response = send_file(
            excel_path,
            as_attachment=True,
            download_name=os.path.basename(excel_path)
        )
        
        @response.call_on_close
        
        def cleanup():
            try:
                os.remove(excel_path)
            except:
                pass
                
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/download-pdf/<reg_no>", methods=["GET"])
def download_pdf(reg_no):
    pdf_path = generate_pdf_report([reg_no])
    
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"error": "PDF generation failed"}), 500

    # Send file as attachment
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"{reg_no}_report.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
