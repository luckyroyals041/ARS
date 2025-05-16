import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_academic_reports():
    """Set up the database extensions needed for academic reports."""
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=os.getenv("host", "localhost"),
            user=os.getenv("user", "lucky"),
            password=os.getenv("password", "#Db@1234"),
            database=os.getenv("database", "reporting_system")
        )
        
        cursor = conn.cursor()
        
        print("Setting up academic reports database extensions...")
        
        # Check if columns exist before adding them
        cursor.execute("SHOW COLUMNS FROM courses LIKE 'subject_type'")
        subject_type_exists = cursor.fetchone() is not None
        
        cursor.execute("SHOW COLUMNS FROM courses LIKE 'course_type'")
        course_type_exists = cursor.fetchone() is not None
        
        # Add subject categorization to courses table if columns don't exist
        if not subject_type_exists:
            cursor.execute("""
                ALTER TABLE courses 
                ADD COLUMN subject_type ENUM('core', 'elective') DEFAULT 'core'
            """)
            print("✅ Added subject_type column to courses table")
        else:
            print("✅ subject_type column already exists")
            
        if not course_type_exists:
            cursor.execute("""
                ALTER TABLE courses 
                ADD COLUMN course_type ENUM('theory', 'lab') DEFAULT 'theory'
            """)
            print("✅ Added course_type column to courses table")
        else:
            print("✅ course_type column already exists")
        
        # Create class average metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS class_averages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                branch VARCHAR(100) NOT NULL,
                semester INT NOT NULL,
                course_code VARCHAR(20) NOT NULL,
                academic_year VARCHAR(10) NOT NULL,
                average_grade_points FLOAT NOT NULL,
                pass_percentage FLOAT NOT NULL,
                FOREIGN KEY (course_code) REFERENCES courses(code)
            )
        """)
        print("✅ Created class_averages table")
        
        # Create subject-semester mapping table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subject_semester_mapping (
                id INT AUTO_INCREMENT PRIMARY KEY,
                course_code VARCHAR(20) NOT NULL,
                semester INT NOT NULL,
                branch VARCHAR(100) NOT NULL,
                academic_year VARCHAR(10) NOT NULL,
                FOREIGN KEY (course_code) REFERENCES courses(code),
                UNIQUE KEY (course_code, semester, branch, academic_year)
            )
        """)
        print("✅ Created subject_semester_mapping table")
        
        # Update courses with subject_type and course_type
        cursor.execute("""
            UPDATE courses
            SET 
                subject_type = CASE 
                    WHEN RAND() > 0.7 THEN 'elective' 
                    ELSE 'core' 
                END,
                course_type = CASE 
                    WHEN RAND() > 0.7 THEN 'lab' 
                    ELSE 'theory' 
                END
            WHERE subject_type IS NULL OR course_type IS NULL
        """)
        print("✅ Updated courses with subject_type and course_type")
        
        # Insert sample data into class_averages
        cursor.execute("""
            INSERT IGNORE INTO class_averages (branch, semester, course_code, academic_year, average_grade_points, pass_percentage)
            SELECT 
                c.department,
                c.semester,
                c.code,
                '2023-24',
                ROUND(RAND() * 3 + 5, 2),  -- Random average between 5 and 8
                ROUND(RAND() * 20 + 80, 1)  -- Random pass percentage between 80% and 100%
            FROM courses c
        """)
        print("✅ Inserted sample data into class_averages table")
        
        # Commit changes
        conn.commit()
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("✅ Academic reports database setup completed successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
        return False
    except Exception as e:
        print(f"❌ Error setting up academic reports database: {e}")
        return False

if __name__ == "__main__":
    setup_academic_reports()