import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_progress_tracking():
    """Set up the database extensions needed for progress tracking reports."""
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host=os.getenv("host", "localhost"),
            user=os.getenv("user", "lucky"),
            password=os.getenv("password", "#Db@1234"),
            database=os.getenv("database", "reporting_system")
        )
        
        cursor = conn.cursor()
        
        print("Setting up progress tracking database extensions...")
        
        # Create curriculum requirements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS curriculum_requirements (
                id INT AUTO_INCREMENT PRIMARY KEY,
                branch VARCHAR(100) NOT NULL,
                semester INT NOT NULL,
                course_code VARCHAR(20) NOT NULL,
                required_credits INT NOT NULL,
                is_mandatory BOOLEAN DEFAULT TRUE,
                category VARCHAR(50) NOT NULL,
                FOREIGN KEY (course_code) REFERENCES courses(code)
            )
        """)
        print("✅ Created curriculum_requirements table")
        
        # Create backlog tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backlog_tracking (
                id INT AUTO_INCREMENT PRIMARY KEY,
                registration_number VARCHAR(20) NOT NULL,
                course_code VARCHAR(20) NOT NULL,
                semester_failed INT NOT NULL,
                attempts INT DEFAULT 1,
                next_attempt_date DATE,
                status ENUM('pending', 'registered', 'cleared') DEFAULT 'pending',
                FOREIGN KEY (registration_number) REFERENCES students(registration_number),
                FOREIGN KEY (course_code) REFERENCES courses(code)
            )
        """)
        print("✅ Created backlog_tracking table")
        
        # Create project/internship data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS internship_projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                registration_number VARCHAR(20) NOT NULL,
                type ENUM('internship', 'project') NOT NULL,
                title VARCHAR(200) NOT NULL,
                organization VARCHAR(200),
                start_date DATE,
                end_date DATE,
                credits INT DEFAULT 0,
                grade VARCHAR(2),
                grade_points FLOAT,
                status ENUM('planned', 'ongoing', 'completed') DEFAULT 'planned',
                description TEXT,
                FOREIGN KEY (registration_number) REFERENCES students(registration_number)
            )
        """)
        print("✅ Created internship_projects table")
        
        # Insert sample data into curriculum_requirements
        cursor.execute("""
            INSERT IGNORE INTO curriculum_requirements (branch, semester, course_code, required_credits, is_mandatory, category)
            SELECT 
                c.department,
                c.semester,
                c.code,
                c.credits,
                TRUE,
                CASE 
                    WHEN c.subject_type = 'core' THEN 'Core'
                    ELSE 'Elective'
                END
            FROM courses c
        """)
        print("✅ Inserted sample data into curriculum_requirements table")
        
        # Insert sample backlog data
        cursor.execute("""
            INSERT IGNORE INTO backlog_tracking (registration_number, course_code, semester_failed, attempts, next_attempt_date, status)
            SELECT 
                g.registration_number,
                g.course_code,
                c.semester,
                1,
                DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 90) DAY),
                'pending'
            FROM grades g
            JOIN courses c ON g.course_code = c.code
            WHERE g.result = 'FAIL'
            LIMIT 20
        """)
        print("✅ Inserted sample data into backlog_tracking table")
        
        # Insert sample internship/project data
        cursor.execute("""
            INSERT IGNORE INTO internship_projects (
                registration_number, type, title, organization, 
                start_date, end_date, credits, grade, grade_points, status, description
            )
            SELECT 
                s.registration_number,
                CASE WHEN RAND() > 0.5 THEN 'internship' ELSE 'project' END,
                CONCAT('Sample ', CASE WHEN RAND() > 0.5 THEN 'Internship' ELSE 'Project' END, ' ', FLOOR(RAND() * 100)),
                CASE 
                    WHEN RAND() > 0.5 THEN 'Tech Solutions Inc.'
                    ELSE 'Innovation Labs'
                END,
                DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 180) DAY),
                DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 180) DAY),
                FLOOR(RAND() * 6) + 2,
                CASE 
                    WHEN RAND() > 0.8 THEN 'A+'
                    WHEN RAND() > 0.6 THEN 'A'
                    WHEN RAND() > 0.4 THEN 'B'
                    WHEN RAND() > 0.2 THEN 'C'
                    ELSE 'D'
                END,
                FLOOR(RAND() * 4) + 6,
                CASE 
                    WHEN RAND() > 0.6 THEN 'completed'
                    WHEN RAND() > 0.3 THEN 'ongoing'
                    ELSE 'planned'
                END,
                'Sample description for the project or internship'
            FROM students s
            LIMIT 20
        """)
        print("✅ Inserted sample data into internship_projects table")
        
        # Commit changes
        conn.commit()
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("✅ Progress tracking database setup completed successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
        return False
    except Exception as e:
        print(f"❌ Error setting up progress tracking database: {e}")
        return False

if __name__ == "__main__":
    setup_progress_tracking()