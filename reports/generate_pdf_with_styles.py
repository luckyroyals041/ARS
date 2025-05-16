import os
import tempfile
import zipfile
import subprocess
import base64
from PyPDF2 import PdfMerger
from database.mysql_data_handler import get_filtered_student_data, get_students_by_reg_nos
from reports.generate_dashboard import generate_histogram
from playwright.sync_api import sync_playwright

def generate_html(student, records, summaries=None, includeCharts=False, template_style="classic"):
    """Reads the HTML template and replaces placeholders with student data and semester records."""

    # Select template based on style
    template_styles = {
        "classic": "pdf_classic.html",
        "modern": "pdf_modern.html",
        "minimal": "pdf_minimal.html"
    }
    
    template_file = template_styles.get(template_style, "pdf_classic.html")
    template_path = os.path.join("templates", template_file)
    
    with open(template_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Format Address in Multi-line Format
    formatted_address = f"""
        <li>{student.get("father_name", "Parent/Guardian")}</li>
        <li>{student.get("door_no", "")}</li>
        <li>{student.get("city", student.get("address", ""))}</li>
        <li>{student.get("mandal", "")}</li>
        <li>{student.get("district", "")}</li>
        <li>{student.get("state", "")}</li>
        <li>{student.get("country", "India")}</li>
        <li>{student.get("pincode", "")}</li>
    """

    # Get the header image path - use the exact path provided
    header_image_path = "/home/lucky/ARS/baggi/main/templates/images/header.png"
    
    # Check if header image exists, if not use a placeholder
    if os.path.exists(header_image_path):
        try:
            with open(header_image_path, "rb") as img_file:
                header_image_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            header_image = f'<img src="data:image/png;base64,{header_image_base64}" alt="College Header" class="header-image">'
            print(f"Header image loaded successfully from {header_image_path}")
        except Exception as e:
            print(f"Error loading header image: {e}")
            header_image = ""
    else:
        print(f"Header image not found at {header_image_path}")
        header_image = ""
    
    # Get student photo based on registration number
    reg_no = student["registered_no"]
    
    # Check for different image formats (jpg, jpeg, png)
    image_formats = ['jpg', 'jpeg', 'png']
    student_photo_abs_path = None
    
    for img_format in image_formats:
        student_photo_path = os.path.join("templates", "images", "students", f"{reg_no}.{img_format}")
        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        temp_path = os.path.join(base_dir, student_photo_path)
        if os.path.exists(temp_path):
            student_photo_abs_path = temp_path
            break
    
    # Check if student photo exists, if not use a placeholder
    if student_photo_abs_path:
        try:
            with open(student_photo_abs_path, "rb") as img_file:
                student_photo_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            img_format = student_photo_abs_path.split('.')[-1]
            student_photo = f'<img src="data:image/{img_format};base64,{student_photo_base64}" alt="Student Photo" style="width:100%;height:100%;object-fit:cover;">'
            print(f"Student photo loaded successfully from {student_photo_abs_path}")
        except Exception as e:
            print(f"Error loading student photo: {e}")
            student_photo = generate_photo_placeholder()
    else:
        print(f"Student photo not found for {reg_no}")
        student_photo = generate_photo_placeholder()

    # Group semester records by semester number
    semester_groups = {}
    for record in records:
        if record["registered_no"] == student["registered_no"]:
            sem_no = record["semester_no"]
            if sem_no not in semester_groups:
                semester_groups[sem_no] = []
            semester_groups[sem_no].append(record)

    # Generate semester tables dynamically
    semester_html = ""
    semester_summary_rows = ""
    semester_summary_html = ""

    for sem_no, courses in sorted(semester_groups.items()):
        total_subjects = len(courses)
        failed_subjects = sum(1 for course in courses if course["result"] == "FAIL")
        sgpa = round(sum(course["grade_points"] for course in courses) / total_subjects, 2) if total_subjects > 0 else 0
        sem_table = f"""
        <br>
        <table class="semester-table" border="1">
            <thead>
                <tr class="semester-header">
                    <td colspan="7">{sem_no} Semester</td>
                </tr>
            </thead>
                <tr>
                    <th>Course Name</th>
                    <th>Month-Year</th>
                    <th>Credits</th>
                    <th>Grade</th>
                    <th>Grade Points</th>
                    <th>Credits Obtained</th>
                    <th>Result</th>
                </tr>
            <tbody>
        """

        for course in courses:
            sem_table += f"""
            <tr>
                <td id = "course_name">{course['course_name']}</td>
                <td>{course['month_year']}</td>
                <td>{course['credits']}</td>
                <td>{course['grade']}</td>
                <td>{course['grade_points']}</td>
                <td>{course['credits_obtained']}</td>
                <td>{course['result']}</td>
            </tr>
            """

        sem_table += "</tbody></table>"
        semester_html += sem_table

        # Collect summary row (instead of creating multiple tables)
        semester_summary_rows += f"""
            <tr>
                <td>{sem_no} Semester</td>
                <td>{total_subjects}</td>
                <td>{failed_subjects}</td>
                <td>{sgpa}</td>
            </tr>
        """

    # Generate Semester Summary Table
    semester_summary_html = f"""
    <br>
    <table class="semester-summary-table" border="1">
        <thead>
            <tr class="semester-header">
                <td colspan="4">Semester Wise Summary</td>
            </tr>
            <tr>
                <th>Semester</th>
                <th>Total Subjects</th>
                <th>Failed Subjects</th>
                <th>SGPA</th>
            </tr>
        </thead>
        <tbody>
            {semester_summary_rows}
        </tbody>
    </table>
    """ if semester_summary_rows else ""
    
    # Generate SGPA data for chart
    sgpa_list = []
    
    # Calculate SGPA from semester records
    for sem_no, courses in sorted(semester_groups.items()):
        total_subjects = len(courses)
        if total_subjects > 0:
            sem_sgpa = round(sum(course["grade_points"] for course in courses) / total_subjects, 2)
            sgpa_list.append(sem_sgpa)
    
    print("SGPA List for chart:", sgpa_list)
    print("Current semester:", student["curr_semester"])
    
    # Only generate chart if we have SGPA data and charts are requested
    dashboard_html = ""
    if sgpa_list and includeCharts:
        dashboard_html = generate_histogram(student["name"], sgpa_list, student["curr_semester"])

    # Replace placeholders with actual data
    html_content = html_content.replace("{{REG_NO}}", student["registered_no"])
    html_content = html_content.replace("{{STUDENT_NAME}}", student["name"])
    html_content = html_content.replace("{{BRANCH}}", student["branch"])
    html_content = html_content.replace("{{SEMESTER}}", f"{student['curr_semester']} Semester")
    html_content = html_content.replace("{{ADDRESS}}", formatted_address)
    html_content = html_content.replace("{{STUDENT_PHOTO}}", student_photo)
    html_content = html_content.replace("{{HEADER_IMAGE}}", header_image)
    html_content = html_content.replace("{{SEMESTER_RECORDS}}", semester_html)
    html_content = html_content.replace("{{SEMESTER_SUMMARY}}", semester_summary_html)
    html_content = html_content.replace("{{Dashboards}}", dashboard_html)
    
    return html_content

def generate_photo_placeholder():
    """Generate a placeholder SVG for missing student photos."""
    student_photo_svg = """
        <svg width="35mm" height="45mm" xmlns="http://www.w3.org/2000/svg">
            <rect width="35mm" height="45mm" fill="#f0f0f0" />
            <circle cx="17.5mm" cy="15mm" r="10mm" fill="#ddd" />
            <rect x="7.5mm" y="25mm" width="20mm" height="20mm" rx="1mm" fill="#ddd" />
            <text x="17.5mm" y="35mm" font-family="Arial" font-size="3mm" text-anchor="middle" fill="#999">Photo</text>
        </svg>
    """
    return f'<img src="data:image/svg+xml;base64,{base64.b64encode(student_photo_svg.encode()).decode()}" alt="Student Photo" style="width:100%;height:100%;">'

def compress_with_ghostscript(input_path, output_path):
    """Compress a PDF file using Ghostscript."""
    command = [
        "gs",  # Linux Ghostscript command
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",  # Balanced quality and size
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path,
    ]
    try:
        subprocess.run(command, check=True)
        print(f"✅ Compressed PDF saved to: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ghostscript compression failed: {e}")
        
def generate_pdf_report(selected_student, includeCharts=False, template_style="classic"):
    """Generates PDF reports for selected students and returns path to a PDF file."""
    # selected_student is already a list
    students, records, summaries = get_students_by_reg_nos(selected_student)

    if not students:
        return None

    student = students[0]
    reg_no = student["registered_no"]
    
    temp_dir = tempfile.gettempdir()
    html_content = generate_html(student, records, summaries, includeCharts, template_style)

    temp_html_path = os.path.join(temp_dir, f"temp_{reg_no}.html")
    pdf_output_path = os.path.join(temp_dir, f"{reg_no}.pdf")

    with open(temp_html_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{temp_html_path}")
        page.pdf(path=pdf_output_path)
        browser.close()

    compressed_pdf_path = os.path.join(temp_dir, f"{reg_no}_report.pdf")
    compress_with_ghostscript(pdf_output_path, compressed_pdf_path)

    # Remove the original PDF and return the compressed one
    os.remove(pdf_output_path)
    os.remove(temp_html_path)
    return compressed_pdf_path

def generate_pdf_reporting(selected_students, generation_type, includeCharts=False, template_style="classic"):
    """
    Generates PDF reports for selected students.
    
    Parameters:
        selected_students (list): List of student registration numbers.
        generation_type (str): 'individual' for individual PDFs, 'combined' for a single merged PDF.
        includeCharts (bool): Whether to include SGPA charts in the PDFs.
        template_style (str): Style of the PDF template ('classic', 'modern', or 'minimal').
    
    Returns:
        str: Path to the generated PDF file or combined PDF file.
    """
    if not selected_students:
        print("⚠️ Please select at least one student by registration number or name.")
        return None

    # Fetch data
    students, records, summaries = get_students_by_reg_nos(selected_students)
    if not students:
        print("⚠️ No student data available for the selected filters.")
        return None

    temp_dir = tempfile.gettempdir()

    if generation_type == 'individual':
        # If only one student, return a single PDF instead of a ZIP
        if len(selected_students) == 1:
            return generate_pdf_report(selected_students, includeCharts, template_style)
        
        # For multiple students, create individual PDFs and return the first one
        pdf_paths = []
        for student in students:
            reg_no = student["registered_no"]
            html_content = generate_html(student, records, None, includeCharts, template_style)
            temp_html_path = os.path.join(temp_dir, f"temp_{reg_no}.html")
            pdf_output_path = os.path.join(temp_dir, f"{reg_no}.pdf")

            # Write HTML
            with open(temp_html_path, "w", encoding="utf-8") as file:
                file.write(html_content)

            # Convert HTML to PDF
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f"file://{temp_html_path}")
                page.pdf(path=pdf_output_path)
                browser.close()

            os.remove(temp_html_path)

            # Compress the generated PDF
            compressed_pdf_path = os.path.join(temp_dir, f"{reg_no}_report.pdf")
            compress_with_ghostscript(pdf_output_path, compressed_pdf_path)
            os.remove(pdf_output_path)
            
            pdf_paths.append(compressed_pdf_path)
        
        # Return the first PDF path
        if pdf_paths:
            return pdf_paths[0]
        return None

    elif generation_type == 'combined':
        individual_pdfs = []
        for student in students:
            html_content = generate_html(student, records, None, includeCharts, template_style)
            reg_no = student["registered_no"]
            temp_html_file = os.path.join(temp_dir, f"temp_{reg_no}.html")
            temp_pdf_file = os.path.join(temp_dir, f"{reg_no}.pdf")

            with open(temp_html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f"file://{temp_html_file}")
                page.pdf(path=temp_pdf_file)
                browser.close()

            individual_pdfs.append(temp_pdf_file)
            os.remove(temp_html_file)

        # Merge PDFs
        merger = PdfMerger()
        for pdf in individual_pdfs:
            merger.append(pdf)

        combined_path = os.path.join(temp_dir, "Combined_Student_Report_temp.pdf")
        merger.write(combined_path)
        merger.close()

        for pdf in individual_pdfs:
            try:
                os.remove(pdf)
            except:
                pass

        # Compress the combined PDF
        compressed_combined_pdf_path = os.path.join(temp_dir, "Combined_Student_Report.pdf")
        compress_with_ghostscript(combined_path, compressed_combined_pdf_path)

        # Make sure the file exists before removing the original
        if os.path.exists(compressed_combined_pdf_path):
            os.remove(combined_path)
            print(f"✅ Combined compressed PDF created: {compressed_combined_pdf_path}")
            return compressed_combined_pdf_path
        else:
            print(f"❌ Failed to create compressed PDF, returning original: {combined_path}")
            return combined_path

    else:
        print("❌ Invalid generation_type. Use 'individual' or 'combined'.")
        return None

if __name__ == "__main__":
    # Example Usage:
    selected_students = ["22A91A6101"]
    path = generate_pdf_report(selected_students, includeCharts=True, template_style="modern")
    print(f"PDF generated at: {path}")