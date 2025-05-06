import os
import tempfile
import zipfile
import subprocess
from PyPDF2 import PdfMerger
from database.fetch_data import fetch_filtered_student_data,fetch_students_by_reg_nos
from playwright.sync_api import sync_playwright

def generate_html(student, records):
    """Reads the HTML template and replaces placeholders with student data and semester records."""

    template_path = os.path.join("templates", "pdf.html")
    with open(template_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Format Address in Multi-line Format
    formatted_address = f"""
        <li><b>To,</b></li>
        <li>{student["father_name"]}</li>
        <li>{student["door_no"]}</li>
        <li>{student["city"]}</li>
        <li>{student["mandal"]}</li>
        <li>{student["district"]}</li>
        <li>{student["state"]}</li>
        <li>{student["country"]}</li>
        <li>{student["pincode"]}</li>
    """

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
        failed_subjects = sum(1 for course in courses if course["result"] == "Fail")
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

    # Replace placeholders with actual data
    html_content = html_content.replace("{{REG_NO}}", student["registered_no"])
    html_content = html_content.replace("{{STUDENT_NAME}}", student["name"])
    html_content = html_content.replace("{{BRANCH}}", student["branch"])
    html_content = html_content.replace("{{SEMESTER}}", f"{student['curr_semester']} Semester")
    html_content = html_content.replace("{{ADDRESS}}", formatted_address)
    html_content = html_content.replace("{{SEMESTER_RECORDS}}", semester_html)
    html_content = html_content.replace("{{SEMESTER_SUMMARY}}", semester_summary_html)
    return html_content

def compress_with_ghostscript(input_path, output_path):
    """Compress a PDF file using Ghostscript."""
    command = [
        "gswin64c",  # or "gs" depending on your environment
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
        
def generate_pdf_report(selected_student):
    """Generates PDF reports for selected students and returns path to a PDF file."""
    # selected_student is already a list
    students, records = fetch_students_by_reg_nos(selected_student)

    if not students:
        return None

    student = students[0]
    reg_no = student["registered_no"]
    
    temp_dir = tempfile.gettempdir()
    html_content = generate_html(student, records)

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

    compressed_pdf_path = os.path.join(temp_dir, f"compressed_{reg_no}.pdf")
    compress_with_ghostscript(pdf_output_path, compressed_pdf_path)

    # Remove the original PDF and return the compressed one
    os.remove(pdf_output_path)
    return compressed_pdf_path



def generate_pdf_reporting(selected_students, generation_type):
    """
    Generates PDF reports for selected students.
    
    Parameters:
        selected_students (list): List of student registration numbers.
        generation_type (str): 'individual' for ZIP of PDFs, 'combined' for a single merged PDF.
    
    Returns:
        str: Path to the generated ZIP or combined PDF file.
    """
    if not selected_students:
        print("⚠️ Please select at least one student by registration number or name.")
        return None

    # Fetch data
    students, records = fetch_filtered_student_data(selected_students)
    if students is None or not students:
        print("⚠️ No student data available for the selected filters.")
        return None

    temp_dir = tempfile.gettempdir()

    if generation_type == 'individual':
        zip_path = os.path.join(temp_dir, "Student_Reports.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for student in students:
                html_content = generate_html(student, records)

                reg_no = student["registered_no"]
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
                compressed_pdf_path = os.path.join(temp_dir, f"compressed_{reg_no}.pdf")
                compress_with_ghostscript(pdf_output_path, compressed_pdf_path)

                # Add the compressed PDF to the ZIP file
                zipf.write(compressed_pdf_path, os.path.basename(compressed_pdf_path))
                os.remove(compressed_pdf_path)

                os.remove(pdf_output_path)

        print(f"✅ ZIP created: {zip_path}")
        return zip_path

    elif generation_type == 'combined':
        individual_pdfs = []
        for student in students:
            html_content = generate_html(student, records)
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

        combined_path = os.path.join(temp_dir, "Combined_Student_Report.pdf")
        merger.write(combined_path)
        merger.close()

        for pdf in individual_pdfs:
            try:
                os.remove(pdf)
            except:
                pass

        # Compress the combined PDF
        compressed_combined_pdf_path = os.path.join(temp_dir, "compressed_Combined_Student_Report.pdf")
        compress_with_ghostscript(combined_path, compressed_combined_pdf_path)

        os.remove(combined_path)

        print(f"✅ Combined compressed PDF created: {compressed_combined_pdf_path}")
        return compressed_combined_pdf_path

    else:
        print("❌ Invalid generation_type. Use 'individual' or 'combined'.")
        return None

if __name__ == "__main__":
    # Example Usage:
    selected_students = ["23A95A6102","23a95a6104"]  # Example: ["23A95A6102", "CHINTHA SITAMAHALAKSHMI"]
    paths = generate_pdf_reporting(selected_students, "individual")
    print(paths)