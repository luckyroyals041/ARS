import mysql.connector
import os

def insert_sample_data():
    """Insert sample student data for testing."""

    conn = mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        database=os.getenv("database"),
    )
    cursor = conn.cursor()

    # Sample Students (Updated to match new table structure)
    students = [
    ("23A95A6102", "AMBATI HARSHITH KUMAR", "Artificial Intelligence And Machine Learning", 4, 
     "KAMESWARA RAO", "D.No:66-1-27/C", "KAKINADA", "S ATCHUTHAPURAM GATE", 
     "EAST GODAVARI", "Andhra Pradesh", "INDIA", "533004"),
     
    ("23A95A6104", "CHINTHA SITAMAHALAKSHMI", "Artificial Intelligence And Machine Learning", 4, 
     "VENKATESWARLU", "D.No:10-2-45", "RAJAHMUNDRY", "KOTHA PETA", 
     "EAST GODAVARI", "Andhra Pradesh", "INDIA", "533101"),
    
    ("23A95A6105", "PRAKASH KUMAR", "Computer Science and Engineering", 5, 
     "SIVARAMAIAH", "D.No:25-1-67", "VISAKHAPATNAM", "MVP COLONY", 
     "VISAKHAPATNAM", "Andhra Pradesh", "INDIA", "530001"),
    
    ("23A95A6106", "RAJESH SHARMA", "Mechanical Engineering", 3, 
     "DURGA PRASAD", "D.No:7-5-45", "GUNTUR", "NEAR BUS STATION", 
     "GUNTUR", "Andhra Pradesh", "INDIA", "522001"),
    
    ("23A95A6107", "SRAVANI KUMARI", "Electrical and Electronics Engineering", 4, 
     "NARASIMHA RAO", "D.No:13-8-56", "TIRUPATI", "SREE RAMA TEMPLE",
     "CHITTOOR", "Andhra Pradesh", "INDIA", "517501"),
    
    ("23A95A6108", "RAVI KUMAR", "Civil Engineering", 4, 
     "SURYANARAYANA", "D.No:12-2-48", "NELLORE", "STREET 12", 
     "NELLORE", "Andhra Pradesh", "INDIA", "524002"),
    
    ("23A95A6109", "SNEHA RANI", "Electronics and Communication Engineering", 6, 
     "VENKATA RAO", "D.No:11-3-60", "KURNOOL", "BANDA ROAD", 
     "KURNOOL", "Andhra Pradesh", "INDIA", "518002"),
    
    ("23A95A6110", "VIKAS REDDY", "Computer Science and Engineering", 2, 
     "VENKATESWARLU", "D.No:3-9-80", "SECUNDERABAD", "NEAR AIRPORT", 
     "HYDERABAD", "Telangana", "INDIA", "500062"),
    
    ("23A95A6111", "NIKHILA RAO", "Artificial Intelligence And Machine Learning", 3, 
     "RAJESH", "D.No:20-1-78", "GUNTUR", "NEAR HOSPITAL", 
     "GUNTUR", "Andhra Pradesh", "INDIA", "522005"),
    
    ("23A95A6112", "ABHISHEK PATEL", "Mechanical Engineering", 5, 
     "RAMA KRISHNA", "D.No:15-9-84", "VIJAYAWADA", "NEAR RAILWAY STATION", 
     "KRISHNA", "Andhra Pradesh", "INDIA", "520001"),
    
    ("23A95A6113", "MANJULA DEVI", "Electrical and Electronics Engineering", 3, 
     "KUMAR", "D.No:8-4-38", "RAJAHMUNDRY", "NEAR KOTHAPETA", 
     "EAST GODAVARI", "Andhra Pradesh", "INDIA", "533103"),
    
    ("23A95A6114", "PRANEETH KUMAR", "Civil Engineering", 5, 
     "SANTHOSH", "D.No:9-1-62", "TIRUPATI", "NEAR TEMPLE", 
     "CHITTOOR", "Andhra Pradesh", "INDIA", "517503"),
    
    ("23A95A6115", "SANDHYA RANI", "Computer Science and Engineering", 2, 
     "NARASIMHA RAO", "D.No:5-3-45", "NELLORE", "NEAR COLLEGE", 
     "NELLORE", "Andhra Pradesh", "INDIA", "524003"),
    
    ("23A95A6116", "MOHAN KUMAR", "Mechanical Engineering", 6, 
     "SURESH", "D.No:10-4-32", "VISAKHAPATNAM", "NEAR BEACH", 
     "VISAKHAPATNAM", "Andhra Pradesh", "INDIA", "530002"),
    
    ("23A95A6117", "RAHUL KUMAR", "Electrical and Electronics Engineering", 2, 
     "VENKATA RAMAIAH", "D.No:17-6-72", "GUNTUR", "NEAR PARK", 
     "GUNTUR", "Andhra Pradesh", "INDIA", "522002")
]

    cursor.executemany(
        """INSERT INTO Students 
           (registered_no, name, branch, curr_semester, father_name, door_no, city, mandal, 
            district, state, country, pincode) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
           ON DUPLICATE KEY UPDATE name=name;""",
        students
    )

    # Sample Semester Records (Multiple Subjects for Each Semester)
    semester_records = [
        # Student 1 - 1st Semester
        ("23A95A6102", 1, "MAY-2023", "Data Structures", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6102", 1, "MAY-2023", "Database Systems", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6102", 1, "MAY-2023", "Computer Networks", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6102", 1, "MAY-2023", "Discrete Mathematics", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6102", 1, "MAY-2023", "Operating Systems", "A", 3.0, 10, 3.0, "Pass"),

        # Student 1 - 2nd Semester
        ("23A95A6102", 2, "DEC-2023", "Machine Learning", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6102", 2, "DEC-2023", "Artificial Intelligence", "C", 4.0, 8, 4.0, "Pass"),
        ("23A95A6102", 2, "DEC-2023", "Computer Vision", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6102", 2, "DEC-2023", "Natural Language Processing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6102", 2, "DEC-2023", "Software Testing", "B", 3.0, 9, 3.0, "Pass"),

        # Student 1 - 3rd Semester
        ("23A95A6102", 3, "MAY-2024", "Cloud Computing", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6102", 3, "MAY-2024", "Cyber Security", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6102", 3, "MAY-2024", "Data Analytics", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6102", 3, "MAY-2024", "Big Data Technologies", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6102", 3, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),

        # Student 2 - 1st Semester
        ("23A95A6104", 1, "MAY-2023", "Operating Systems", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6104", 1, "MAY-2023", "Software Engineering", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6104", 1, "MAY-2023", "Mathematics-II", "F", 3.0, 0, 0.0, "Fail"),  # Failed Subject
        ("23A95A6104", 1, "MAY-2023", "Computer Organization", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6104", 1, "MAY-2023", "Theory of Computation", "B", 3.0, 9, 3.0, "Pass"),

        # Student 2 - 2nd Semester
        ("23A95A6104", 2, "DEC-2023", "Machine Learning", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6104", 2, "DEC-2023", "Artificial Intelligence", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6104", 2, "DEC-2023", "Cyber Security", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6104", 2, "DEC-2023", "Data Analytics", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6104", 2, "DEC-2023", "Software Testing", "A", 3.0, 10, 3.0, "Pass"),

        # Student 2 - 3rd Semester
        ("23A95A6104", 3, "MAY-2024", "Cloud Computing", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6104", 3, "MAY-2024", "Blockchain Technology", "C", 4.0, 8, 4.0, "Pass"),
        ("23A95A6104", 3, "MAY-2024", "Big Data Technologies", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6104", 3, "MAY-2024", "Internet of Things", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6104", 3, "MAY-2024", "Quantum Computing", "C", 3.0, 8, 3.0, "Pass"),

        # Student 3 - 1st Semester
        ("23A95A6105", 1, "MAY-2023", "Operating Systems", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6105", 1, "MAY-2023", "Software Engineering", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6105", 1, "MAY-2023", "Discrete Mathematics", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6105", 1, "MAY-2023", "Mathematics-II", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6105", 1, "MAY-2023", "Computer Organization", "A", 3.0, 10, 3.0, "Pass"),

        # Student 3 - 2nd Semester
        ("23A95A6105", 2, "DEC-2023", "Machine Learning", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6105", 2, "DEC-2023", "Artificial Intelligence", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6105", 2, "DEC-2023", "Computer Networks", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6105", 2, "DEC-2023", "Data Analytics", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6105", 2, "DEC-2023", "Cloud Computing", "A", 3.0, 10, 3.0, "Pass"),

        # Student 3 - 3rd Semester
        ("23A95A6105", 3, "MAY-2024", "Cyber Security", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6105", 3, "MAY-2024", "Big Data Technologies", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6105", 3, "MAY-2024", "Quantum Computing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6105", 3, "MAY-2024", "Internet of Things", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6105", 3, "MAY-2024", "Data Analytics", "B", 3.0, 9, 3.0, "Pass"),
        
        # Student 3 - 4th Semester
        ("23A95A6105", 4, "MAY-2023", "Data Structures", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6105", 4, "MAY-2023", "Software Engineering", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6105", 4, "MAY-2023", "Discrete Mathematics", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6105", 4, "MAY-2023", "Theory of Computation", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6105", 4, "MAY-2023", "Computer Organization", "A", 3.0, 10, 3.0, "Pass"),

        # Student 4 - 1st Semester
        ("23A95A6106", 1, "DEC-2023", "Machine Learning", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6106", 1, "DEC-2023", "Artificial Intelligence", "C", 4.0, 8, 4.0, "Pass"),
        ("23A95A6106", 1, "DEC-2023", "Cloud Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6106", 1, "DEC-2023", "Data Analytics", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6106", 1, "DEC-2023", "Cyber Security", "B", 3.0, 9, 3.0, "Pass"),

        # Student 4 - 2nd Semester
        ("23A95A6106", 2, "MAY-2024", "Artificial Intelligence", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6106", 2, "MAY-2024", "Blockchain Technology", "C", 4.0, 8, 4.0, "Pass"),
        ("23A95A6106", 2, "MAY-2024", "Software Testing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6106", 2, "MAY-2024", "Data Analytics", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6106", 2, "MAY-2024", "Big Data Technologies", "B", 3.0, 9, 3.0, "Pass"),
        
        # Student 5 - 1st Semester
        ("23A95A6107", 1, "MAY-2023", "Data Structures", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6107", 1, "MAY-2023", "Database Systems", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6107", 1, "MAY-2023", "Operating Systems", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6107", 1, "MAY-2023", "Computer Networks", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6107", 1, "MAY-2023", "Discrete Mathematics", "B", 3.0, 9, 3.0, "Pass"),

        # Student 5 - 2nd Semester
        ("23A95A6107", 2, "DEC-2023", "Machine Learning", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6107", 2, "DEC-2023", "Artificial Intelligence", "C", 4.0, 8, 4.0, "Pass"),
        ("23A95A6107", 2, "DEC-2023", "Cloud Computing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6107", 2, "DEC-2023", "Data Analytics", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6107", 2, "DEC-2023", "Blockchain Technology", "B", 3.0, 9, 3.0, "Pass"),

        # Student 5 - 3rd Semester
        ("23A95A6107", 3, "MAY-2024", "Artificial Intelligence", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6107", 3, "MAY-2024", "Big Data Technologies", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6107", 3, "MAY-2024", "Cyber Security", "C", 4.0, 8, 4.0, "Pass"),
        ("23A95A6107", 3, "MAY-2024", "Internet of Things", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6107", 3, "MAY-2024", "Quantum Computing", "B", 3.0, 9, 3.0, "Pass"),

        # Student 6 - 1st Semester
        ("23A95A6108", 1, "MAY-2023", "Data Structures", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6108", 1, "MAY-2023", "Discrete Mathematics", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6108", 1, "MAY-2023", "Theory of Computation", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6108", 1, "MAY-2023", "Mathematics-II", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6108", 1, "MAY-2023", "Computer Organization", "B", 3.0, 9, 3.0, "Pass"),

        # Student 6 - 2nd Semester
        ("23A95A6108", 2, "DEC-2023", "Machine Learning", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6108", 2, "DEC-2023", "Artificial Intelligence", "C", 4.0, 8, 4.0, "Pass"),
        ("23A95A6108", 2, "DEC-2023", "Cloud Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6108", 2, "DEC-2023", "Cyber Security", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6108", 2, "DEC-2023", "Data Analytics", "A", 3.0, 10, 3.0, "Pass"),

        # Student 6 - 3rd Semester
        ("23A95A6108", 3, "MAY-2024", "Artificial Intelligence", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6108", 3, "MAY-2024", "Data Analytics", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6108", 3, "MAY-2024", "Big Data Technologies", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6108", 3, "MAY-2024", "Quantum Computing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6108", 3, "MAY-2024", "Software Testing", "A", 3.0, 10, 3.0, "Pass"),

        # Student 7 - 1st Semester
        ("23A95A6109", 1, "MAY-2023", "Operating Systems", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6109", 1, "MAY-2023", "Software Engineering", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6109", 1, "MAY-2023", "Mathematics-II", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6109", 1, "MAY-2023", "Computer Networks", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6109", 1, "MAY-2023", "Discrete Mathematics", "A", 3.0, 10, 3.0, "Pass"),

        # Student 7 - 2nd Semester
        ("23A95A6109", 2, "DEC-2023", "Machine Learning", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6109", 2, "DEC-2023", "Artificial Intelligence", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6109", 2, "DEC-2023", "Cloud Computing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6109", 2, "DEC-2023", "Data Analytics", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6109", 2, "DEC-2023", "Cyber Security", "B", 3.0, 9, 3.0, "Pass"),

        # Student 7 - 3rd Semester
        ("23A95A6109", 3, "MAY-2024", "Artificial Intelligence", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6109", 3, "MAY-2024", "Data Analytics", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6109", 3, "MAY-2024", "Quantum Computing", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6109", 3, "MAY-2024", "Internet of Things", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6109", 3, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),
        
        # Student 7 - 4th Semester
        ("23A95A6109", 4, "MAY-2023", "Data Structures", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6109", 4, "MAY-2023", "Discrete Mathematics", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6109", 4, "MAY-2023", "Mathematics-II", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6109", 4, "MAY-2023", "Computer Organization", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6109", 4, "MAY-2023", "Theory of Computation", "A", 3.0, 10, 3.0, "Pass"),
        
        # Student 7 - 5th Semester
        ("23A95A6109", 5, "DEC-2023", "Artificial Intelligence", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6109", 5, "DEC-2023", "Machine Learning", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6109", 5, "DEC-2023", "Cloud Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6109", 5, "DEC-2023", "Big Data Technologies", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6109", 5, "DEC-2023", "Cyber Security", "A", 3.0, 10, 3.0, "Pass"),

        # Student 8 - 4th Semester
        ("23A95A6110", 1, "MAY-2024", "Data Analytics", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6110", 1, "MAY-2024", "Blockchain Technology", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6110", 1, "MAY-2024", "Internet of Things", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6110", 1, "MAY-2024", "Quantum Computing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6110", 1, "MAY-2024", "Artificial Intelligence", "C", 3.0, 8, 3.0, "Pass"),

        # Student 9 - 1st Semester
        ("23A95A6111", 1, "MAY-2023", "Data Structures", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6111", 1, "MAY-2023", "Database Systems", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6111", 1, "MAY-2023", "Operating Systems", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6111", 1, "MAY-2023", "Computer Networks", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6111", 1, "MAY-2023", "Discrete Mathematics", "B", 3.0, 9, 3.0, "Pass"),

        # Student 9 - 2nd Semester
        ("23A95A6111", 2, "DEC-2023", "Machine Learning", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6111", 2, "DEC-2023", "Artificial Intelligence", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6111", 2, "DEC-2023", "Cloud Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6111", 2, "DEC-2023", "Data Analytics", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6111", 2, "DEC-2023", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),

        # Student 10 - 1st Semester
        ("23A95A6112", 1, "MAY-2024", "Artificial Intelligence", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6112", 1, "MAY-2024", "Big Data Technologies", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6112", 1, "MAY-2024", "Cyber Security", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6112", 1, "MAY-2024", "Internet of Things", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6112", 1, "MAY-2024", "Quantum Computing", "A", 3.0, 10, 3.0, "Pass"),

        # Student 10 - 2nd Semester
        ("23A95A6112", 2, "MAY-2023", "Mathematics-II", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6112", 2, "MAY-2023", "Theory of Computation", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6112", 2, "MAY-2023", "Computer Organization", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6112", 2, "MAY-2023", "Software Engineering", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6112", 2, "MAY-2023", "Operating Systems", "A", 3.0, 10, 3.0, "Pass"),

        # Student 10 - 3rd Semester
        ("23A95A6112", 3, "DEC-2023", "Machine Learning", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6112", 3, "DEC-2023", "Artificial Intelligence", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6112", 3, "DEC-2023", "Cloud Computing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6112", 3, "DEC-2023", "Data Analytics", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6112", 3, "DEC-2023", "Cyber Security", "B", 3.0, 9, 3.0, "Pass"),

        # Student 10 - 4th Semester
        ("23A95A6112", 4, "MAY-2024", "Artificial Intelligence", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6112", 4, "MAY-2024", "Big Data Technologies", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6112", 4, "MAY-2024", "Data Analytics", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6112", 4, "MAY-2024", "Internet of Things", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6112", 4, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),

        # Student 11 - 1st Semester
        ("23A95A6113", 1, "MAY-2023", "Data Structures", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6113", 1, "MAY-2023", "Discrete Mathematics", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6113", 1, "MAY-2023", "Computer Organization", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6113", 1, "MAY-2023", "Software Engineering", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6113", 1, "MAY-2023", "Mathematics-II", "B", 3.0, 9, 3.0, "Pass"),

        # Student 11 - 2nd Semester
        ("23A95A6113", 2, "DEC-2023", "Artificial Intelligence", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6113", 2, "DEC-2023", "Machine Learning", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6113", 2, "DEC-2023", "Cloud Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6113", 2, "DEC-2023", "Big Data Technologies", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6113", 2, "DEC-2023", "Cyber Security", "A", 3.0, 10, 3.0, "Pass"),

        # Student 12 - 1st Semester
        ("23A95A6114", 1, "MAY-2024", "Data Analytics", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6114", 1, "MAY-2024", "Blockchain Technology", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6114", 1, "MAY-2024", "Internet of Things", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6114", 1, "MAY-2024", "Quantum Computing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6114", 1, "MAY-2024", "DevOps", "A", 3.0, 10, 3.0, "Pass"),

        # Student 12 - 2nd Semester
        ("23A95A6114", 2, "MAY-2023", "Data Structures", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6114", 2, "MAY-2023", "Discrete Mathematics", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6114", 2, "MAY-2023", "Computer Organization", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6114", 2, "MAY-2023", "Software Engineering", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6114", 2, "MAY-2023", "Mathematics-II", "C", 3.0, 8, 3.0, "Pass"),

        # Student 12 - 3rd Semester
        ("23A95A6114", 3, "DEC-2023", "Artificial Intelligence", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6114", 3, "DEC-2023", "Machine Learning", "C", 4.0, 8, 4.0, "Pass"),
        ("23A95A6114", 3, "DEC-2023", "Cloud Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6114", 3, "DEC-2023", "Big Data Technologies", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6114", 3, "DEC-2023", "Cyber Security", "B", 3.0, 9, 3.0, "Pass"),

        # Student 12 - 4th Semester
        ("23A95A6114", 4, "MAY-2024", "Data Analytics", "B", 4.0, 9, 4.0, "Pass"),
        ("23A95A6114", 4, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6114", 4, "MAY-2024", "Internet of Things", "C", 3.0, 8, 3.0, "Pass"),
        ("23A95A6114", 4, "MAY-2024", "Quantum Computing", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6114", 4, "MAY-2024", "DevOps", "C", 3.0, 8, 3.0, "Pass"),

        # Student 13 - 1st Semester
        ("23A95A6115", 1, "MAY-2023", "Data Structures", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6115", 1, "MAY-2023", "Discrete Mathematics", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6115", 1, "MAY-2023", "Computer Organization", "B", 3.0, 9, 3.0, "Pass"),
        ("23A95A6115", 1, "MAY-2023", "Software Engineering", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6115", 1, "MAY-2023", "Mathematics-II", "A", 3.0, 10, 3.0, "Pass"),


        # Student 14 - 1st Semester
        ("23A95A6116", 1, "MAY-2024", "Data Analytics", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6116", 1, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 1, "MAY-2024", "Internet of Things", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 1, "MAY-2024", "Quantum Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 1, "MAY-2024", "DevOps", "A", 3.0, 10, 3.0, "Pass"),
        
        # Student 14 - 2nd Semester
        ("23A95A6116", 2, "MAY-2024", "Data Analytics", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6116", 2, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 2, "MAY-2024", "Internet of Things", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 2, "MAY-2024", "Quantum Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 2, "MAY-2024", "DevOps", "A", 3.0, 10, 3.0, "Pass"),
        
        # Student 14 - 3rd Semester
        ("23A95A6116", 3, "MAY-2024", "Data Analytics", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6116", 3, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 3, "MAY-2024", "Internet of Things", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 3, "MAY-2024", "Quantum Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 3, "MAY-2024", "DevOps", "A", 3.0, 10, 3.0, "Pass"),
        
        # Student 14 - 4th Semester
        ("23A95A6116", 4, "MAY-2024", "Data Analytics", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6116", 4, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 4, "MAY-2024", "Internet of Things", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 4, "MAY-2024", "Quantum Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 4, "MAY-2024", "DevOps", "A", 3.0, 10, 3.0, "Pass"),
        
        # Student 14 - 5th Semester
        ("23A95A6116", 5, "MAY-2024", "Data Analytics", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6116", 5, "MAY-2024", "Blockchain Technology", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 5, "MAY-2024", "Internet of Things", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 5, "MAY-2024", "Quantum Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6116", 5, "MAY-2024", "DevOps", "A", 3.0, 10, 3.0, "Pass"),

        # Student 15 - 1st Semester
        ("23A95A6117", 1, "DEC-2023", "Artificial Intelligence", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6117", 1, "DEC-2023", "Machine Learning", "A", 4.0, 10, 4.0, "Pass"),
        ("23A95A6117", 1, "DEC-2023", "Cloud Computing", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6117", 1, "DEC-2023", "Big Data Technologies", "A", 3.0, 10, 3.0, "Pass"),
        ("23A95A6117", 1, "DEC-2023", "Cyber Security", "A", 3.0, 10, 3.0, "Pass"),
    ]


    cursor.executemany(
        """INSERT INTO SemesterRecords 
           (registered_no, semester_no, month_year, course_name, grade, credits, grade_points, credits_obtained, result) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
        semester_records
    )


    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Sample data inserted successfully!")

if __name__ == "__main__":
    insert_sample_data()        
