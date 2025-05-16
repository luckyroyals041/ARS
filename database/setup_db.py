import mysql.connector

# Connect to MySQL Server
connection = mysql.connector.connect(
    host="localhost",
    user="lucky",
    password="#Db@1234"
)

cursor = connection.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS StudentReportingDB;")
cursor.execute("USE StudentReportingDB;")

# Create Students Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    registered_no VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    curr_semester INT NOT NULL,
    father_name VARCHAR(100) NOT NULL,
    door_no VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    mandal VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    cgpa DECIMAL(4,2) DEFAULT 0
);
""")

# Create Semester Records Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS SemesterRecords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registered_no VARCHAR(20) NOT NULL,
    semester_no INT NOT NULL,
    month_year VARCHAR(10) NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    grade VARCHAR(2),
    credits DECIMAL(2,1),
    grade_points INT,
    credits_obtained DECIMAL(2,1),
    result ENUM('Pass', 'Fail') NOT NULL,
    FOREIGN KEY (registered_no) REFERENCES Students(registered_no) ON DELETE CASCADE
);
""")

# Create Semester Summary Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS SemesterSummary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registered_no VARCHAR(20) NOT NULL,
    semester_no INT NOT NULL,
    total_no_of_subjects INT NOT NULL,
    sgpa DECIMAL(4,2) NOT NULL,
    no_of_failed_subjects INT NOT NULL,
    FOREIGN KEY (registered_no) REFERENCES Students(registered_no) ON DELETE CASCADE,
    UNIQUE KEY unique_semester (registered_no, semester_no)
);
""")

# Triggers (run separately since Python connector doesn't support DELIMITER)
print("\n⚠️ Please run the following SQL statements manually in the MySQL shell:\n")
print("""
DELIMITER //
CREATE TRIGGER update_cgpa_after_semester_update
AFTER INSERT ON SemesterRecords
FOR EACH ROW
BEGIN
    UPDATE Students s
    SET s.cgpa = (
        SELECT COALESCE(AVG(sr.grade_points), 0)
        FROM SemesterRecords sr
        WHERE sr.registered_no = s.registered_no
    )
    WHERE s.registered_no = NEW.registered_no;
END;//

CREATE TRIGGER update_semester_summary_after_insert
AFTER INSERT ON SemesterRecords
FOR EACH ROW
BEGIN
    INSERT INTO SemesterSummary (registered_no, semester_no, total_no_of_subjects, sgpa, no_of_failed_subjects)
    VALUES (
        NEW.registered_no,
        NEW.semester_no,
        (SELECT COUNT(*) FROM SemesterRecords WHERE registered_no = NEW.registered_no AND semester_no = NEW.semester_no),
        (SELECT COALESCE(AVG(grade_points), 0) FROM SemesterRecords WHERE registered_no = NEW.registered_no AND semester_no = NEW.semester_no),
        (SELECT COUNT(*) FROM SemesterRecords WHERE registered_no = NEW.registered_no AND semester_no = NEW.semester_no AND result = 'Fail')
    )
    ON DUPLICATE KEY UPDATE
        total_no_of_subjects = VALUES(total_no_of_subjects),
        sgpa = VALUES(sgpa),
        no_of_failed_subjects = VALUES(no_of_failed_subjects);
END;//
DELIMITER ;
""")

# Close the connection
cursor.close()
connection.close()
print("✅ Tables created successfully. Don't forget to run the triggers in MySQL shell!")
