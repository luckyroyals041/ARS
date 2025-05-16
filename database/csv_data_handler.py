import os
import pandas as pd
import json
from collections import defaultdict

# Path to data files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
STUDENTS_FILE = os.path.join(DATA_DIR, 'students.csv')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.csv')
GRADES_FILE = os.path.join(DATA_DIR, 'grades.csv')

def load_students():
    """Load student data from CSV file"""
    try:
        if not os.path.exists(STUDENTS_FILE):
            print(f"Warning: Students file not found at {STUDENTS_FILE}")
            return []
            
        df = pd.read_csv(STUDENTS_FILE)
        # Rename columns to match the expected format in the application
        df = df.rename(columns={
            'registration_number': 'registered_no',
            'name': 'name',
            'branch': 'branch',
            'current_semester': 'curr_semester',
            'address': 'address'
        })
        
        # Split address into components (simplified approach)
        df['door_no'] = 'Door No.'  # Placeholder
        df['city'] = df['address']  # Use address as city
        df['mandal'] = 'Mandal'     # Placeholder
        df['district'] = 'District' # Placeholder
        df['state'] = 'State'       # Placeholder
        df['country'] = 'India'     # Default
        df['pincode'] = '500000'    # Placeholder
        df['father_name'] = 'Parent/Guardian'  # Placeholder
        
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading student data: {e}")
        return []

def load_courses():
    """Load course data from CSV file"""
    try:
        if not os.path.exists(COURSES_FILE):
            print(f"Warning: Courses file not found at {COURSES_FILE}")
            return []
            
        df = pd.read_csv(COURSES_FILE)
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading course data: {e}")
        return []

def load_grades():
    """Load grades data from CSV file"""
    try:
        if not os.path.exists(GRADES_FILE):
            print(f"Warning: Grades file not found at {GRADES_FILE}")
            return []
            
        df = pd.read_csv(GRADES_FILE)
        # Rename columns to match the expected format in the application
        df = df.rename(columns={
            'registration_number': 'registered_no',
            'course_code': 'course_code',
            'grade': 'grade',
            'grade_points': 'grade_points',
            'credits_obtained': 'credits_obtained',
            'result': 'result',
            'month_year': 'month_year'
        })
        return df.to_dict('records')
    except Exception as e:
        print(f"Error loading grades data: {e}")
        return []

def get_student_data():
    """Get all student data with their records and summaries"""
    students = load_students()
    grades = load_grades()
    courses = {course['code']: course for course in load_courses()}
    
    # Process grades to create semester records
    records = []
    for grade in grades:
        course_code = grade['course_code']
        if course_code in courses:
            course = courses[course_code]
            record = {
                'registered_no': grade['registered_no'],
                'semester_no': course['semester'],
                'month_year': grade['month_year'],
                'course_name': course['name'],
                'grade': grade['grade'],
                'credits': course['credits'],
                'grade_points': grade['grade_points'],
                'credits_obtained': grade['credits_obtained'],
                'result': 'Pass' if grade['result'] == 'PASS' else 'Fail'
            }
            records.append(record)
    
    # Generate semester summaries
    summaries = []
    student_semester_grades = defaultdict(lambda: defaultdict(list))
    
    for record in records:
        key = (record['registered_no'], record['semester_no'])
        student_semester_grades[key].append(record)
    
    for (reg_no, sem_no), sem_records in student_semester_grades.items():
        total_subjects = len(sem_records)
        failed_subjects = sum(1 for r in sem_records if r['result'] == 'Fail')
        
        # Calculate SGPA
        total_grade_points = sum(r['grade_points'] * float(r['credits']) for r in sem_records)
        total_credits = sum(float(r['credits']) for r in sem_records)
        sgpa = round(total_grade_points / total_credits, 2) if total_credits > 0 else 0
        
        summary = {
            'registered_no': reg_no,
            'semester_no': sem_no,
            'total_no_of_subjects': total_subjects,
            'no_of_failed_subjects': failed_subjects,
            'sgpa': sgpa
        }
        summaries.append(summary)
    
    return students, records, summaries

def get_filtered_student_data(selected_students=None, choose_semester=None, branch=None):
    """Get filtered student data based on criteria"""
    students, records, summaries = get_student_data()
    
    filtered_students = students
    
    # Filter by branch
    if branch:
        filtered_students = [s for s in filtered_students if s['branch'] == branch]
    
    # Filter by semester
    if choose_semester:
        filtered_students = [s for s in filtered_students if s['curr_semester'] == int(choose_semester)]
    
    # Filter by selected students
    if selected_students:
        filtered_students = [s for s in filtered_students if s['registered_no'] in selected_students]
    
    # Filter records for the filtered students
    filtered_records = [r for r in records if r['registered_no'] in [s['registered_no'] for s in filtered_students]]
    
    return filtered_students, filtered_records

def get_students_by_reg_nos(reg_nos):
    """Get student details and records for specific registration numbers"""
    if not reg_nos:
        return [], [], []
    
    students, records, summaries = get_student_data()
    
    filtered_students = [s for s in students if s['registered_no'] in reg_nos]
    filtered_records = [r for r in records if r['registered_no'] in reg_nos]
    filtered_summaries = [s for s in summaries if s['registered_no'] in reg_nos]
    
    return filtered_students, filtered_records, filtered_summaries

# For testing
if __name__ == "__main__":
    students, records, summaries = get_student_data()
    print(f"Loaded {len(students)} students")
    print(f"Loaded {len(records)} records")
    print(f"Generated {len(summaries)} summaries")
    
    # Print first student
    if students:
        print("\nFirst student:")
        print(json.dumps(students[0], indent=2))
    
    # Print first record
    if records:
        print("\nFirst record:")
        print(json.dumps(records[0], indent=2))
    
    # Print first summary
    if summaries:
        print("\nFirst summary:")
        print(json.dumps(summaries[0], indent=2))