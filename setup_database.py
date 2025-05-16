import os
import mysql.connector
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

def setup_database():
    """Set up the database and tables if they don't exist."""
    try:
        # Connect to MySQL server without specifying a database
        conn = mysql.connector.connect(
            host=os.getenv("host", "localhost"),
            user=os.getenv("user", "root"),
            password=os.getenv("password", "")
        )
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        db_name = os.getenv("database", "reporting_system")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ Database '{db_name}' created or already exists")
        
        # Switch to the database
        cursor.execute(f"USE {db_name}")
        
        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                registration_number VARCHAR(20) NOT NULL UNIQUE,
                branch VARCHAR(100) NOT NULL,
                current_semester INT NOT NULL,
                address VARCHAR(255),
                father_name VARCHAR(255),
                door_no VARCHAR(100),
                city VARCHAR(100),
                mandal VARCHAR(100),
                district VARCHAR(100),
                state VARCHAR(100),
                country VARCHAR(100),
                pincode VARCHAR(20),
                email VARCHAR(100),
                phone VARCHAR(20),
                date_of_birth DATE,
                gender ENUM('Male', 'Female', 'Other'),
                blood_group VARCHAR(10),
                admission_year INT,
                cgpa DECIMAL(4,2) DEFAULT 0.0
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'students' created or already exists")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                code VARCHAR(20) NOT NULL UNIQUE,
                credits INT NOT NULL,
                semester INT NOT NULL,
                department VARCHAR(100) NOT NULL,
                subject_type ENUM('core', 'elective') DEFAULT 'core',
                course_type ENUM('theory', 'lab') DEFAULT 'theory'
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'courses' created or already exists")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                id INT AUTO_INCREMENT PRIMARY KEY,
                registration_number VARCHAR(20) NOT NULL,
                course_code VARCHAR(20) NOT NULL,
                grade VARCHAR(5) NOT NULL,
                grade_points FLOAT NOT NULL,
                credits_obtained INT NOT NULL,
                result VARCHAR(10) NOT NULL,
                month_year VARCHAR(20) NOT NULL,
                FOREIGN KEY (registration_number) REFERENCES students(registration_number) ON DELETE CASCADE,
                FOREIGN KEY (course_code) REFERENCES courses(code) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'grades' created or already exists")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semester_summary (
                id INT AUTO_INCREMENT PRIMARY KEY,
                registered_no VARCHAR(20) NOT NULL,
                semester_no INT NOT NULL,
                total_no_of_subjects INT NOT NULL,
                sgpa DECIMAL(4,2) NOT NULL,
                no_of_failed_subjects INT NOT NULL,
                FOREIGN KEY (registered_no) REFERENCES students(registration_number) ON DELETE CASCADE,
                UNIQUE KEY unique_semester (registered_no, semester_no)
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'semester_summary' created or already exists")
        
        # Create achievements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                achievement_type ENUM('academic', 'sports', 'cultural', 'technical', 'other') NOT NULL,
                achievement_date DATE,
                issuing_organization VARCHAR(255),
                certificate_url VARCHAR(255),
                verified BOOLEAN DEFAULT FALSE,
                verified_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'achievements' created or already exists")
        
        # Create certifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS certifications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                certification_type ENUM('technical', 'soft_skills', 'language', 'professional', 'other') NOT NULL,
                issuing_organization VARCHAR(255) NOT NULL,
                issue_date DATE,
                expiry_date DATE,
                credential_id VARCHAR(100),
                certificate_url VARCHAR(255),
                verified BOOLEAN DEFAULT FALSE,
                verified_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'certifications' created or already exists")
        
        # Create communications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS communications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_id INT NOT NULL,
                recipient_id INT,
                recipient_group VARCHAR(100),
                subject VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                communication_type ENUM('announcement', 'message', 'notification') NOT NULL,
                read_status BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'communications' created or already exists")
        
        # Create faculty_student_mapping table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faculty_student_mapping (
                id INT AUTO_INCREMENT PRIMARY KEY,
                faculty_id INT NOT NULL,
                student_id INT NOT NULL,
                assigned_date DATE NOT NULL,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (faculty_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                UNIQUE KEY unique_mapping (faculty_id, student_id)
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'faculty_student_mapping' created or already exists")
        
        # Create departments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                code VARCHAR(20) NOT NULL UNIQUE,
                hod_id INT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'departments' created or already exists")
        
        # Create events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                event_type ENUM('meeting', 'exam', 'deadline', 'other') NOT NULL,
                start_date DATETIME NOT NULL,
                end_date DATETIME NOT NULL,
                location VARCHAR(255),
                created_by INT NOT NULL,
                department_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'events' created or already exists")
        
        # Create counseling_sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS counseling_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                faculty_id INT NOT NULL,
                student_id INT NOT NULL,
                session_date DATE NOT NULL,
                notes TEXT,
                action_items TEXT,
                follow_up_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (faculty_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'counseling_sessions' created or already exists")
        
        # Create report_templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS report_templates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                template_type ENUM('individual', 'batch', 'department', 'custom') NOT NULL,
                template_data JSON NOT NULL,
                created_by INT NOT NULL,
                is_public BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'report_templates' created or already exists")
        
        # Create scheduled_reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                template_id INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                schedule_type ENUM('daily', 'weekly', 'monthly', 'once') NOT NULL,
                schedule_day INT,
                schedule_time TIME NOT NULL,
                next_run DATETIME NOT NULL,
                parameters JSON,
                recipients TEXT,
                created_by INT NOT NULL,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (template_id) REFERENCES report_templates(id) ON DELETE CASCADE,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'scheduled_reports' created or already exists")
        
        # Create generated_reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generated_reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                template_id INT,
                scheduled_report_id INT,
                report_name VARCHAR(255) NOT NULL,
                report_type ENUM('pdf', 'excel', 'html') NOT NULL,
                file_path VARCHAR(255) NOT NULL,
                parameters JSON,
                generated_by INT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (template_id) REFERENCES report_templates(id) ON DELETE SET NULL,
                FOREIGN KEY (scheduled_report_id) REFERENCES scheduled_reports(id) ON DELETE SET NULL,
                FOREIGN KEY (generated_by) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB
        """)
        print("✅ Table 'generated_reports' created or already exists")
        
        # Import auth models and create users table
        from auth.models import create_users_table
        create_users_table()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database setup completed successfully")
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    setup_database()