#!/usr/bin/env python3
"""
Script to convert CSV data into SQL INSERT statements.
This script handles student data, course data, and grades data from CSV files.
"""

import csv
import os

def read_csv_file(file_path):
    """Read CSV file and return data as a list of dictionaries."""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return []
        
    result = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result.append(row)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
        
    return result

def generate_student_sql(students, db_type='mysql'):
    """Generate SQL INSERT statements for student data."""
    sql_statements = []
    
    for student in students:
        values = [
            f"'{student['name'].replace(\"'\", \"''\")}'"
            f"'{student['registration_number']}'"
            f"'{student['branch'].replace(\"'\", \"''\")}'"
            f"{student['current_semester']}"
            f"'{student['address'].replace(\"'\", \"''\")}'"
        ]
        
        if db_type.lower() == 'mysql':
            # Use INSERT IGNORE for MySQL to skip duplicates
            sql = f"INSERT IGNORE INTO students (name, registration_number, branch, current_semester, address) " \
                  f"VALUES ({', '.join(values)});"
        else:
            # For SQLite, use INSERT OR IGNORE
            sql = f"INSERT OR IGNORE INTO students (name, registration_number, branch, current_semester, address) " \
                  f"VALUES ({', '.join(values)});"
        
        sql_statements.append(sql)
    
    return sql_statements

def generate_course_sql(courses, db_type='mysql'):
    """Generate SQL INSERT statements for course data."""
    sql_statements = []
    
    for course in courses:
        values = [
            f"'{course['name'].replace(\"'\", \"''\")}'"
            f"'{course['code']}'"
            f"{course['credits']}"
            f"{course['semester']}"
            f"'{course['department'].replace(\"'\", \"''\")}'"
        ]
        
        if db_type.lower() == 'mysql':
            # Use INSERT IGNORE for MySQL to skip duplicates
            sql = f"INSERT IGNORE INTO courses (name, code, credits, semester, department) " \
                  f"VALUES ({', '.join(values)});"
        else:
            # For SQLite, use INSERT OR IGNORE
            sql = f"INSERT OR IGNORE INTO courses (name, code, credits, semester, department) " \
                  f"VALUES ({', '.join(values)});"
        
        sql_statements.append(sql)
    
    return sql_statements

def generate_grade_sql(grades, db_type='mysql'):
    """Generate SQL INSERT statements for grade data."""
    sql_statements = []
    
    for grade in grades:
        values = [
            f"'{grade['registration_number']}'"
            f"'{grade['course_code']}'"
            f"'{grade['grade']}'"
            f"{grade['grade_points']}"
            f"{grade['credits_obtained']}"
            f"'{grade['result']}'"
            f"'{grade['month_year']}'"
        ]
        
        if db_type.lower() == 'mysql':
            # Use INSERT IGNORE for MySQL to skip duplicates
            sql = f"INSERT IGNORE INTO grades (registration_number, course_code, grade, grade_points, " \
                  f"credits_obtained, result, month_year) VALUES ({', '.join(values)});"
        else:
            # For SQLite, use INSERT OR IGNORE
            sql = f"INSERT OR IGNORE INTO grades (registration_number, course_code, grade, grade_points, " \
                  f"credits_obtained, result, month_year) VALUES ({', '.join(values)});"
        
        sql_statements.append(sql)
    
    return sql_statements

def generate_create_tables_sql(db_type='mysql'):
    """Generate SQL CREATE TABLE statements.
    
    Args:
        db_type: Database type ('mysql' or 'sqlite')
    """
    sql_statements = []
    
    # Add DROP TABLE statements first
    if db_type.lower() == 'mysql':
        sql_statements.append("""
-- Drop existing tables in reverse order of dependencies
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
        """.strip())
    else:
        sql_statements.append("""
-- Drop existing tables in reverse order of dependencies
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
        """.strip())
    
    if db_type.lower() == 'mysql':
        # Students table for MySQL
        sql_statements.append("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    registration_number VARCHAR(20) NOT NULL UNIQUE,
    branch VARCHAR(100) NOT NULL,
    current_semester INT NOT NULL,
    address VARCHAR(255)
) ENGINE=InnoDB;
        """.strip())
        
        # Courses table for MySQL
        sql_statements.append("""
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    credits INT NOT NULL,
    semester INT NOT NULL,
    department VARCHAR(100) NOT NULL
) ENGINE=InnoDB;
        """.strip())
        
        # Grades table for MySQL
        sql_statements.append("""
CREATE TABLE IF NOT EXISTS grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration_number VARCHAR(20) NOT NULL,
    course_code VARCHAR(20) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    grade_points FLOAT NOT NULL,
    credits_obtained INT NOT NULL,
    result VARCHAR(10) NOT NULL,
    month_year VARCHAR(20) NOT NULL,
    FOREIGN KEY (registration_number) REFERENCES students(registration_number),
    FOREIGN KEY (course_code) REFERENCES courses(code)
) ENGINE=InnoDB;
        """.strip())
    else:
        # SQLite tables
        # Students table
        sql_statements.append("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    registration_number TEXT NOT NULL UNIQUE,
    branch TEXT NOT NULL,
    current_semester INTEGER NOT NULL,
    address TEXT
);
        """.strip())
        
        # Courses table
        sql_statements.append("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    credits INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    department TEXT NOT NULL
);
        """.strip())
        
        # Grades table
        sql_statements.append("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL,
    course_code TEXT NOT NULL,
    grade TEXT NOT NULL,
    grade_points REAL NOT NULL,
    credits_obtained INTEGER NOT NULL,
    result TEXT NOT NULL,
    month_year TEXT NOT NULL,
    FOREIGN KEY (registration_number) REFERENCES students(registration_number),
    FOREIGN KEY (course_code) REFERENCES courses(code)
);
        """.strip())
    
    return sql_statements

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert CSV data to SQL INSERT statements')
    parser.add_argument('--students', default='students.csv', help='Path to students CSV file')
    parser.add_argument('--courses', default='courses.csv', help='Path to courses CSV file')
    parser.add_argument('--grades', default='grades.csv', help='Path to grades CSV file')
    parser.add_argument('--output', default='insert_data.sql', help='Output SQL file path')
    parser.add_argument('--db-type', default='mysql', choices=['mysql', 'sqlite'], 
                        help='Database type (mysql or sqlite)')
    parser.add_argument('--drop-tables', action='store_true', 
                        help='Include DROP TABLE statements before CREATE TABLE')
    
    args = parser.parse_args()
    
    # Read data from CSV files
    print(f"Reading student data from {args.students}...")
    students = read_csv_file(args.students)
    
    print(f"Reading course data from {args.courses}...")
    courses = read_csv_file(args.courses)
    
    print(f"Reading grade data from {args.grades}...")
    grades = read_csv_file(args.grades)
    
    # Generate SQL statements
    create_tables_sql = generate_create_tables_sql(args.db_type)
    student_sql = generate_student_sql(students, args.db_type)
    course_sql = generate_course_sql(courses, args.db_type)
    grade_sql = generate_grade_sql(grades, args.db_type)
    
    # Save SQL to file
    with open(args.output, 'w') as f:
        f.write("-- Create Tables\n")
        for sql in create_tables_sql:
            f.write(sql + "\n\n")
        
        f.write("\n-- Insert Student Data\n")
        for sql in student_sql:
            f.write(sql + "\n")
        
        f.write("\n-- Insert Course Data\n")
        for sql in course_sql:
            f.write(sql + "\n")
        
        f.write("\n-- Insert Grade Data\n")
        for sql in grade_sql:
            f.write(sql + "\n")
    
    print(f"\nSQL statements have been saved to '{args.output}'")
    print(f"Processed {len(students)} students, {len(courses)} courses, and {len(grades)} grades.")

if __name__ == "__main__":
    main()