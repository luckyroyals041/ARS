import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database name from environment variables, with fallback
db_name = os.getenv("DATABASE") or os.getenv("database", "reporting_system")

# Helper to get DB connection using env vars
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        database=db_name
    )

def check_database():
    """Check if the database exists, if not, run setup_db.py."""
    if os.getenv("host") is None or os.getenv("user") is None or os.getenv("password") is None:
        print("⚠️ Environment variables for database connection are not set.")
        return
    conn = mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password")
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES;")
    databases = [db[0] for db in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    if db_name not in databases:
        print(f"⚠️ Database {db_name} not found. Running setup_db.py...")
        import database.setup_db

def fetch_student_data():
    """Fetch student details, semester records, and semester summary from MySQL."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT registered_no, name, branch, curr_semester, 
               father_name, door_no, city, mandal, district, 
               state, country, pincode 
        FROM Students;
    """)
    students = cursor.fetchall()

    cursor.execute("""
        SELECT registered_no, semester_no, month_year, course_name, 
               grade, credits, grade_points, credits_obtained, result
        FROM SemesterRecords;
    """)
    records = cursor.fetchall()

    cursor.execute("""
        SELECT registered_no, semester_no, total_no_of_subjects, 
               no_of_failed_subjects, sgpa
        FROM SemesterSummary;
    """)
    summaries = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return students, records, summaries

def fetch_students_by_reg_nos(reg_nos):
    """Fetch student details and semester records for multiple students."""
    if not reg_nos:
        return [], []

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    format_strings = ','.join(['%s'] * len(reg_nos))

    cursor.execute(f"""
        SELECT registered_no, name, branch, curr_semester, 
               father_name, door_no, city, mandal, district, 
               state, country, pincode 
        FROM Students
        WHERE registered_no IN ({format_strings});
    """, tuple(reg_nos))
    students = cursor.fetchall()

    cursor.execute(f"""
        SELECT registered_no, semester_no, month_year, course_name, 
               grade, credits, grade_points, credits_obtained, result
        FROM SemesterRecords
        WHERE registered_no IN ({format_strings});
    """, tuple(reg_nos))
    records = cursor.fetchall()

    cursor.execute(f"""
        SELECT registered_no, semester_no, total_no_of_subjects, 
               no_of_failed_subjects, sgpa
        FROM SemesterSummary;
        WHERE registered_no IN ({format_strings});
    """, tuple(reg_nos))
    summaries = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return students, records, summaries

def fetch_filtered_student_data(selected_students=None, choose_semester=None, branch=None):
    """Fetch filtered student details and their semester records from MySQL."""
    if not selected_students and choose_semester is None and branch is None:
        return None, None

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    where_clauses = []
    params = []

    if choose_semester:
        where_clauses.append("curr_semester = %s")
        params.append(choose_semester)

    if branch:
        where_clauses.append("branch = %s")
        params.append(branch)

    if selected_students:
        reg_no_conditions = []
        name_conditions = []
        
        for student in selected_students:
            if any(c.isdigit() for c in student):
                reg_no_conditions.append("registered_no = %s")
                params.append(student)
            else:
                name_conditions.append("LOWER(name) = LOWER(%s)")
                params.append(student)
        
        conditions = []
        if reg_no_conditions:
            conditions.append(f"({' OR '.join(reg_no_conditions)})")
        if name_conditions:
            conditions.append(f"({' OR '.join(name_conditions)})")
        
        if conditions:
            where_clauses.append(f"({' OR '.join(conditions)})")

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    print("\nDebug - SQL Query:", f"SELECT * FROM Students WHERE {where_sql}")
    print("Debug - Parameters:", params)

    cursor.execute(f"""
        SELECT COUNT(*) as count
        FROM Students
        WHERE {where_sql};
    """, params)
    count_result = cursor.fetchone()
    
    if count_result['count'] == 0:
        cursor.close()
        conn.close()
        return None, None

    cursor.execute(f"""
        SELECT registered_no, name, branch, curr_semester, 
               father_name, door_no, city, mandal, district, 
               state, country, pincode 
        FROM Students
        WHERE {where_sql};
    """, params)
    students = cursor.fetchall()

    registered_nos = [student['registered_no'] for student in students]
    
    placeholders = ', '.join(['%s'] * len(registered_nos))
    cursor.execute(f"""
        SELECT registered_no, semester_no, month_year, course_name, 
               grade, credits, grade_points, credits_obtained, result
        FROM SemesterRecords
        WHERE registered_no IN ({placeholders});
    """, registered_nos)
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return students, records

if __name__ == "__main__":
    selected_students = ["23A95A6102", "23A95A6104"]
    choose_semester = ""
    branch = ""
    std, rec = fetch_filtered_student_data(selected_students, choose_semester, branch)
    print("\nStudents filtered: ", std)