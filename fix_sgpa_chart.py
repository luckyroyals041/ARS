#!/usr/bin/env python3
"""
Script to fix SGPA chart generation in PDF reports.
"""

import os
import sys
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_semester_summary_table():
    """Create and populate the SemesterSummary table."""
    print("Creating and populating SemesterSummary table...")
    
    conn = mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        database=os.getenv("database")
    )
    cursor = conn.cursor()

    # Create SemesterSummary table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SemesterSummary (
        id INT AUTO_INCREMENT PRIMARY KEY,
        registered_no VARCHAR(20) NOT NULL,
        semester_no INT NOT NULL,
        total_no_of_subjects INT NOT NULL,
        no_of_failed_subjects INT NOT NULL,
        sgpa DECIMAL(4,2) NOT NULL,
        FOREIGN KEY (registered_no) REFERENCES Students(registered_no) ON DELETE CASCADE,
        UNIQUE KEY unique_semester (registered_no, semester_no)
    );
    """)

    # Get all students
    cursor.execute("SELECT registered_no FROM Students;")
    students = cursor.fetchall()

    # For each student, calculate semester summary
    for student in students:
        reg_no = student[0]
        
        # Get all semesters for this student
        cursor.execute("""
        SELECT DISTINCT semester_no 
        FROM SemesterRecords 
        WHERE registered_no = %s;
        """, (reg_no,))
        
        semesters = cursor.fetchall()
        
        for semester in semesters:
            sem_no = semester[0]
            
            # Count total subjects in this semester
            cursor.execute("""
            SELECT COUNT(*) 
            FROM SemesterRecords 
            WHERE registered_no = %s AND semester_no = %s;
            """, (reg_no, sem_no))
            
            total_subjects = cursor.fetchone()[0]
            
            # Count failed subjects
            cursor.execute("""
            SELECT COUNT(*) 
            FROM SemesterRecords 
            WHERE registered_no = %s AND semester_no = %s AND result = 'Fail';
            """, (reg_no, sem_no))
            
            failed_subjects = cursor.fetchone()[0]
            
            # Calculate SGPA
            cursor.execute("""
            SELECT AVG(grade_points) 
            FROM SemesterRecords 
            WHERE registered_no = %s AND semester_no = %s;
            """, (reg_no, sem_no))
            
            sgpa = round(cursor.fetchone()[0], 2)
            
            # Insert or update semester summary
            cursor.execute("""
            INSERT INTO SemesterSummary 
            (registered_no, semester_no, total_no_of_subjects, no_of_failed_subjects, sgpa)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            total_no_of_subjects = %s,
            no_of_failed_subjects = %s,
            sgpa = %s;
            """, (reg_no, sem_no, total_subjects, failed_subjects, sgpa, 
                 total_subjects, failed_subjects, sgpa))

    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ SemesterSummary table created and populated successfully.")

def update_generate_pdf_file():
    """Update the generate_pdf.py file to handle missing SGPA data."""
    print("Updating generate_pdf.py file...")
    
    file_path = os.path.join("reports", "generate_pdf.py")
    
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Find the section that generates the SGPA chart
    start_marker = "    sgpa_list = []"
    end_marker = "    dashboard_html = generate_histogram(student[\"name\"], sgpa_list,student[\"curr_semester\"])"
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker) + len(end_marker)
        
        # Replace with improved code
        new_code = """    # Generate SGPA data for chart
    sgpa_list = []
    
    # Calculate SGPA from semester records
    for sem_no, courses in sorted(semester_groups.items()):
        total_subjects = len(courses)
        if total_subjects > 0:
            sem_sgpa = round(sum(course["grade_points"] for course in courses) / total_subjects, 2)
            sgpa_list.append(sem_sgpa)
    
    print("SGPA List for chart:", sgpa_list)
    print("Current semester:", student["curr_semester"])
    
    # Only generate chart if we have SGPA data
    dashboard_html = ""
    if sgpa_list:
        dashboard_html = generate_histogram(student["name"], sgpa_list, student["curr_semester"])"""
        
        updated_content = content[:start_idx] + new_code + content[end_idx:]
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(updated_content)
        
        print("✅ generate_pdf.py updated successfully.")
    else:
        print("❌ Could not find the SGPA chart generation code in generate_pdf.py.")
        return False
    
    return True

def main():
    """Main function to fix SGPA chart issues."""
    print("Starting SGPA chart fix...")
    
    # Step 1: Create and populate SemesterSummary table
    create_semester_summary_table()
    
    # Step 2: Update generate_pdf.py file
    if update_generate_pdf_file():
        print("\n✅ SGPA chart fix completed successfully.")
        print("\nYou can now generate PDF reports with SGPA charts.")
        print("Run the test_pdf_generation.py script to verify:")
        print("  ./test_pdf_generation.py")
    else:
        print("\n❌ SGPA chart fix failed.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())