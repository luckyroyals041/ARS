import mysql.connector
import os
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

# Get database name from environment variables, with fallback
db_name = os.getenv("DATABASE") or os.getenv("database", "reporting_system")

# Print environment variables for debugging
print(f"Database connection details:")
print(f"Host: {os.getenv('host', 'localhost')}")
print(f"User: {os.getenv('user', 'root')}")
print(f"Database name from env: {db_name}")

# Helper to get DB connection using env vars
def get_connection():
    try:
        # Explicitly use the db_name variable
        conn = mysql.connector.connect(
            host=os.getenv("host", "localhost"),
            user=os.getenv("user", "root"),
            password=os.getenv("password", ""),
            database=db_name
        )
        print(f"Connected to database: {db_name}")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        traceback.print_exc()
        return None

def check_database():
    """Check if the database exists and is accessible."""
    try:
        conn = get_connection()
        if conn and conn.is_connected():
            print("✅ Database connection successful")
            
            # Check if tables exist using a regular cursor
            regular_cursor = conn.cursor()
            regular_cursor.execute("SHOW TABLES")
            tables = [table[0] for table in regular_cursor.fetchall()]
            print(f"Tables in database: {tables}")
            
            regular_cursor.close()
            conn.close()
            return True
        else:
            print("❌ Failed to connect to database")
            return False
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        traceback.print_exc()
        return False

def get_student_data():
    """Get all student data with their records and summaries."""
    try:
        conn = get_connection()
        if not conn:
            return [], [], []
            
        cursor = conn.cursor(dictionary=True)

        # Check if tables exist using a regular cursor
        regular_cursor = conn.cursor()
        regular_cursor.execute("SHOW TABLES")
        tables = [table[0] for table in regular_cursor.fetchall()]
        regular_cursor.close()
        
        print(f"Tables in database: {tables}")
        
        # Use the correct table names based on what's in the database
        students_table = "students"
        grades_table = "grades"
        courses_table = "courses"
        
        # Fetch students
        try:
            cursor.execute(f"""
                SELECT 
                    id,
                    name,
                    registration_number AS registered_no,
                    branch,
                    current_semester AS curr_semester,
                    address,
                    address AS door_no,
                    address AS city,
                    'Mandal' AS mandal,
                    'District' AS district,
                    'State' AS state,
                    'India' AS country,
                    '500000' AS pincode,
                    'Parent/Guardian' AS father_name
                FROM {students_table}
            """)
            students = cursor.fetchall()
            print(f"Fetched {len(students)} students")
        except mysql.connector.Error as err:
            print(f"Error fetching students: {err}")
            students = []

        # Fetch grades with course details
        try:
            cursor.execute(f"""
                SELECT 
                    g.registration_number AS registered_no,
                    c.semester AS semester_no,
                    g.month_year,
                    c.name AS course_name,
                    g.grade,
                    c.credits,
                    g.grade_points,
                    g.credits_obtained,
                    g.result
                FROM {grades_table} g
                JOIN {courses_table} c ON g.course_code = c.code
            """)
            records = cursor.fetchall()
            print(f"Fetched {len(records)} grade records")
        except mysql.connector.Error as err:
            print(f"Error fetching grades: {err}")
            records = []

        # Generate semester summaries
        summaries = []
        
        try:
            # Get unique student-semester combinations
            cursor.execute(f"""
                SELECT DISTINCT 
                    g.registration_number, 
                    c.semester
                FROM {grades_table} g
                JOIN {courses_table} c ON g.course_code = c.code
            """)
            student_semesters = cursor.fetchall()
            
            # For each student-semester, calculate summary
            for item in student_semesters:
                reg_no = item['registration_number']
                sem_no = item['semester']
                
                # Count total subjects
                cursor.execute(f"""
                    SELECT COUNT(*) AS total
                    FROM {grades_table} g
                    JOIN {courses_table} c ON g.course_code = c.code
                    WHERE g.registration_number = %s AND c.semester = %s
                """, (reg_no, sem_no))
                total_subjects = cursor.fetchone()['total']
                
                # Count failed subjects
                cursor.execute(f"""
                    SELECT COUNT(*) AS failed
                    FROM {grades_table} g
                    JOIN {courses_table} c ON g.course_code = c.code
                    WHERE g.registration_number = %s AND c.semester = %s AND UPPER(g.result) = 'FAIL'
                """, (reg_no, sem_no))
                failed_subjects = cursor.fetchone()['failed']
                
                # Calculate SGPA
                cursor.execute(f"""
                    SELECT AVG(g.grade_points) AS sgpa
                    FROM {grades_table} g
                    JOIN {courses_table} c ON g.course_code = c.code
                    WHERE g.registration_number = %s AND c.semester = %s
                """, (reg_no, sem_no))
                sgpa_result = cursor.fetchone()
                sgpa = round(sgpa_result['sgpa'], 2) if sgpa_result['sgpa'] else 0
                
                # Add to summaries
                summaries.append({
                    'registered_no': reg_no,
                    'semester_no': sem_no,
                    'total_no_of_subjects': total_subjects,
                    'no_of_failed_subjects': failed_subjects,
                    'sgpa': sgpa
                })
            
            print(f"Generated {len(summaries)} semester summaries")
        except mysql.connector.Error as err:
            print(f"Error generating summaries: {err}")

        cursor.close()
        conn.close()
        
        return students, records, summaries
        
    except Exception as e:
        print(f"Error in get_student_data: {e}")
        traceback.print_exc()
        return [], [], []

def get_filtered_student_data(selected_students=None, choose_semester=None, branch=None):
    """Get filtered student data based on criteria."""
    try:
        conn = get_connection()
        if not conn:
            return [], []
            
        cursor = conn.cursor(dictionary=True)
        
        # Check if tables exist using a regular cursor
        regular_cursor = conn.cursor()
        regular_cursor.execute("SHOW TABLES")
        tables = [table[0] for table in regular_cursor.fetchall()]
        regular_cursor.close()
        
        # Use the correct table names based on what's in the database
        students_table = "students"
        grades_table = "grades"
        courses_table = "courses"
        
        # Build the WHERE clause
        where_clauses = []
        params = []
        
        if choose_semester:
            where_clauses.append("current_semester = %s")
            params.append(int(choose_semester))
            
        if branch:
            where_clauses.append("branch = %s")
            params.append(branch)
            
        if selected_students:
            placeholders = ', '.join(['%s'] * len(selected_students))
            where_clauses.append(f"registration_number IN ({placeholders})")
            params.extend(selected_students)
            
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        # Fetch filtered students
        query = f"""
            SELECT 
                id,
                name,
                registration_number AS registered_no,
                branch,
                current_semester AS curr_semester,
                address,
                address AS door_no,
                address AS city,
                'Mandal' AS mandal,
                'District' AS district,
                'State' AS state,
                'India' AS country,
                '500000' AS pincode,
                'Parent/Guardian' AS father_name
            FROM {students_table}
            WHERE {where_sql}
        """
        
        cursor.execute(query, params)
        students = cursor.fetchall()
        
        # If no students found, return empty results
        if not students:
            cursor.close()
            conn.close()
            return [], []
            
        # Get registration numbers for filtered students
        reg_nos = [student['registered_no'] for student in students]
        
        # Fetch grades for these students
        placeholders = ', '.join(['%s'] * len(reg_nos))
        cursor.execute(f"""
            SELECT 
                g.registration_number AS registered_no,
                c.semester AS semester_no,
                g.month_year,
                c.name AS course_name,
                g.grade,
                c.credits,
                g.grade_points,
                g.credits_obtained,
                g.result
            FROM {grades_table} g
            JOIN {courses_table} c ON g.course_code = c.code
            WHERE g.registration_number IN ({placeholders})
        """, reg_nos)
        records = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return students, records
        
    except Exception as e:
        print(f"Error in get_filtered_student_data: {e}")
        traceback.print_exc()
        return [], []

def get_students_by_reg_nos(reg_nos):
    """Get student details and records for specific registration numbers."""
    if not reg_nos:
        return [], [], []
        
    try:
        conn = get_connection()
        if not conn:
            return [], [], []
            
        cursor = conn.cursor(dictionary=True)
        
        # Check if tables exist using a regular cursor
        regular_cursor = conn.cursor()
        regular_cursor.execute("SHOW TABLES")
        tables = [table[0] for table in regular_cursor.fetchall()]
        regular_cursor.close()
        
        # Use the correct table names based on what's in the database
        students_table = "students"
        grades_table = "grades"
        courses_table = "courses"
        
        # Fetch students
        placeholders = ', '.join(['%s'] * len(reg_nos))
        cursor.execute(f"""
            SELECT 
                id,
                name,
                registration_number AS registered_no,
                branch,
                current_semester AS curr_semester,
                address,
                address AS door_no,
                address AS city,
                'Mandal' AS mandal,
                'District' AS district,
                'State' AS state,
                'India' AS country,
                '500000' AS pincode,
                'Parent/Guardian' AS father_name
            FROM {students_table}
            WHERE registration_number IN ({placeholders})
        """, reg_nos)
        students = cursor.fetchall()
        
        # Fetch grades
        cursor.execute(f"""
            SELECT 
                g.registration_number AS registered_no,
                c.semester AS semester_no,
                g.month_year,
                c.name AS course_name,
                g.grade,
                c.credits,
                g.grade_points,
                g.credits_obtained,
                g.result
            FROM {grades_table} g
            JOIN {courses_table} c ON g.course_code = c.code
            WHERE g.registration_number IN ({placeholders})
        """, reg_nos)
        records = cursor.fetchall()
        
        # Generate summaries
        summaries = []
        
        # For each student and semester, calculate summary
        for reg_no in reg_nos:
            # Get semesters for this student
            cursor.execute(f"""
                SELECT DISTINCT c.semester
                FROM {grades_table} g
                JOIN {courses_table} c ON g.course_code = c.code
                WHERE g.registration_number = %s
            """, (reg_no,))
            semesters = [row['semester'] for row in cursor.fetchall()]
            
            for sem_no in semesters:
                # Count total subjects
                cursor.execute(f"""
                    SELECT COUNT(*) AS total
                    FROM {grades_table} g
                    JOIN {courses_table} c ON g.course_code = c.code
                    WHERE g.registration_number = %s AND c.semester = %s
                """, (reg_no, sem_no))
                total_subjects = cursor.fetchone()['total']
                
                # Count failed subjects
                cursor.execute(f"""
                    SELECT COUNT(*) AS failed
                    FROM {grades_table} g
                    JOIN {courses_table} c ON g.course_code = c.code
                    WHERE g.registration_number = %s AND c.semester = %s AND UPPER(g.result) = 'FAIL'
                """, (reg_no, sem_no))
                failed_subjects = cursor.fetchone()['failed']
                
                # Calculate SGPA
                cursor.execute(f"""
                    SELECT AVG(g.grade_points) AS sgpa
                    FROM {grades_table} g
                    JOIN {courses_table} c ON g.course_code = c.code
                    WHERE g.registration_number = %s AND c.semester = %s
                """, (reg_no, sem_no))
                sgpa_result = cursor.fetchone()
                sgpa = round(sgpa_result['sgpa'], 2) if sgpa_result['sgpa'] else 0
                
                # Add to summaries
                summaries.append({
                    'registered_no': reg_no,
                    'semester_no': sem_no,
                    'total_no_of_subjects': total_subjects,
                    'no_of_failed_subjects': failed_subjects,
                    'sgpa': sgpa
                })
        
        cursor.close()
        conn.close()
        
        return students, records, summaries
        
    except Exception as e:
        print(f"Error in get_students_by_reg_nos: {e}")
        traceback.print_exc()
        return [], [], []

# For testing
if __name__ == "__main__":
    if check_database():
        students, records, summaries = get_student_data()
        print(f"Loaded {len(students)} students")
        print(f"Loaded {len(records)} records")
        print(f"Generated {len(summaries)} summaries")
        
        # Print first student
        if students:
            print("\nFirst student:")
            print(students[0])
        
        # Print first record
        if records:
            print("\nFirst record:")
            print(records[0])
        
        # Print first summary
        if summaries:
            print("\nFirst summary:")
            print(summaries[0])