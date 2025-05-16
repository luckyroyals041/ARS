import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_semester_summary_table():
    """Create the SemesterSummary table if it doesn't exist and populate it with data."""
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

if __name__ == "__main__":
    create_semester_summary_table()