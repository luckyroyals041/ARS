import mysql.connector
from database.db_config import DB_CONFIG

def check_database():
    """Check if the database exists, if not, run setup_db.py."""
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES;")
    databases = [db[0] for db in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    if "StudentReportingDB" not in databases:
        print("⚠️ Database not found. Running setup_db.py...")
        import database.setup_db

def fetch_student_data():
    """Fetch student details, semester records, and semester summary from MySQL."""
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # Fetch student details including full address
    cursor.execute("""
        SELECT registered_no, name, branch, curr_semester, 
               father_name, door_no, city, mandal, district, 
               state, country, pincode 
        FROM Students;
    """)
    students = cursor.fetchall()

    # Fetch semester records (individual subjects per semester)
    cursor.execute("""
        SELECT registered_no, semester_no, month_year, course_name, 
               grade, credits, grade_points, credits_obtained, result
        FROM SemesterRecords;
    """)
    records = cursor.fetchall()

    # Fetch semester summary (overall performance per semester)
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

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    format_strings = ','.join(['%s'] * len(reg_nos))

    # Fetch student details
    cursor.execute(f"""
        SELECT registered_no, name, branch, curr_semester, 
               father_name, door_no, city, mandal, district, 
               state, country, pincode 
        FROM Students
        WHERE registered_no IN ({format_strings});
    """, tuple(reg_nos))
    students = cursor.fetchall()

    # Fetch semester records
    cursor.execute(f"""
        SELECT registered_no, semester_no, month_year, course_name, 
               grade, credits, grade_points, credits_obtained, result
        FROM SemesterRecords
        WHERE registered_no IN ({format_strings});
    """, tuple(reg_nos))
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return students, records


def fetch_filtered_student_data(selected_students=None, choose_semester=None, branch=None):
    """Fetch filtered student details and their semester records from MySQL."""
    
    # Validate inputs
    if not selected_students and choose_semester is None and branch is None:
        return None, None  # Return None to indicate no filters provided
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # Build the WHERE clause based on filters
    where_clauses = []
    params = []
    
    # First apply semester filter if provided
    if choose_semester is not None and choose_semester != "":
        where_clauses.append("curr_semester = %s")
        params.append(choose_semester)

    # Then apply branch filter if provided
    if branch is not None and branch != "":
        where_clauses.append("branch = %s")
        params.append(branch)

    # Finally apply student filter if provided
    if selected_students:
        # Handle both registration numbers and names
        reg_no_conditions = []
        name_conditions = []
        
        for student in selected_students:
            # If it looks like a registration number (contains numbers)
            if any(c.isdigit() for c in student):
                # Use exact matching for registration numbers
                reg_no_conditions.append("registered_no = %s")
                params.append(student)
            # Otherwise treat as a name
            else:
                # Use case-insensitive exact matching for names
                name_conditions.append("LOWER(name) = LOWER(%s)")
                params.append(student)
        
        # Combine conditions
        conditions = []
        if reg_no_conditions:
            conditions.append(f"({' OR '.join(reg_no_conditions)})")
        if name_conditions:
            conditions.append(f"({' OR '.join(name_conditions)})")
        
        if conditions:
            where_clauses.append(f"({' OR '.join(conditions)})")

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Debug: Print the query and parameters
    print("\nDebug - SQL Query:", f"SELECT * FROM Students WHERE {where_sql}")
    print("Debug - Parameters:", params)
    
    # First check if any students match the filters
    cursor.execute(f"""
        SELECT COUNT(*) as count
        FROM Students
        WHERE {where_sql};
    """, params)
    count_result = cursor.fetchone()
    
    if count_result['count'] == 0:
        cursor.close()
        conn.close()
        return None, None  # Return None to indicate no students match the filters

    # Fetch filtered student details
    cursor.execute(f"""
        SELECT registered_no, name, branch, curr_semester, 
               father_name, door_no, city, mandal, district, 
               state, country, pincode 
        FROM Students
        WHERE {where_sql};
    """, params)
    students = cursor.fetchall()

    # Get registered numbers of filtered students
    registered_nos = [student['registered_no'] for student in students]
    
    # Fetch semester records only for filtered students
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
    selected_students = ["23A95A6102","23A95A6104"]
    choose_semester = ""
    branch = ""
    std, rec = fetch_filtered_student_data(selected_students, choose_semester, branch)
    print("\nStudents filtered: ", std)

