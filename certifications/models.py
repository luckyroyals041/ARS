from database.mysql_data_handler import get_connection
import traceback

def get_student_certifications(student_id=None, verified_only=False):
    """Get certifications for a specific student or all certifications."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT c.*, s.name as student_name, s.registration_number, 
                   u.first_name as verifier_first_name, u.last_name as verifier_last_name
            FROM certifications c
            JOIN students s ON c.student_id = s.id
            LEFT JOIN users u ON c.verified_by = u.id
            WHERE 1=1
        """
        params = []
        
        if student_id:
            query += " AND c.student_id = %s"
            params.append(student_id)
        
        if verified_only:
            query += " AND c.verified = TRUE"
        
        query += " ORDER BY c.issue_date DESC"
        
        cursor.execute(query, params)
        certifications = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return certifications
        
    except Exception as e:
        print(f"Error in get_student_certifications: {e}")
        traceback.print_exc()
        return []

def get_certification_by_id(certification_id):
    """Get a specific certification by ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT c.*, s.name as student_name, s.registration_number, 
                   u.first_name as verifier_first_name, u.last_name as verifier_last_name
            FROM certifications c
            JOIN students s ON c.student_id = s.id
            LEFT JOIN users u ON c.verified_by = u.id
            WHERE c.id = %s
        """
        
        cursor.execute(query, (certification_id,))
        certification = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return certification
        
    except Exception as e:
        print(f"Error in get_certification_by_id: {e}")
        traceback.print_exc()
        return None

def create_certification(certification_data):
    """Create a new certification."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO certifications (
                student_id, title, description, certification_type, 
                issuing_organization, issue_date, expiry_date, 
                credential_id, certificate_url, verified
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            certification_data['student_id'],
            certification_data['title'],
            certification_data.get('description', None),
            certification_data['certification_type'],
            certification_data['issuing_organization'],
            certification_data.get('issue_date', None),
            certification_data.get('expiry_date', None),
            certification_data.get('credential_id', None),
            certification_data.get('certificate_url', None),
            certification_data.get('verified', False)
        ))
        
        certification_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return certification_id
        
    except Exception as e:
        print(f"Error in create_certification: {e}")
        traceback.print_exc()
        return None

def update_certification(certification_id, certification_data):
    """Update an existing certification."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build the SET clause dynamically based on provided fields
        set_clause = []
        params = []
        
        for key, value in certification_data.items():
            if key != 'id':  # Skip the ID field
                set_clause.append(f"{key} = %s")
                params.append(value)
        
        # Add the certification_id to the parameters
        params.append(certification_id)
        
        # Execute the update query
        cursor.execute(f"""
            UPDATE certifications
            SET {', '.join(set_clause)}
            WHERE id = %s
        """, params)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error in update_certification: {e}")
        traceback.print_exc()
        return False

def verify_certification(certification_id, verified_by):
    """Verify a certification."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE certifications
            SET verified = TRUE, verified_by = %s
            WHERE id = %s
        """
        
        cursor.execute(query, (verified_by, certification_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error in verify_certification: {e}")
        traceback.print_exc()
        return False

def delete_certification(certification_id):
    """Delete a certification."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM certifications WHERE id = %s"
        
        cursor.execute(query, (certification_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error in delete_certification: {e}")
        traceback.print_exc()
        return False

def get_certification_stats():
    """Get certification statistics."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get total certifications count
        cursor.execute("SELECT COUNT(*) as total FROM certifications")
        total = cursor.fetchone()['total']
        
        # Get verified certifications count
        cursor.execute("SELECT COUNT(*) as verified FROM certifications WHERE verified = TRUE")
        verified = cursor.fetchone()['verified']
        
        # Get certifications by type
        cursor.execute("""
            SELECT certification_type, COUNT(*) as count
            FROM certifications
            GROUP BY certification_type
        """)
        by_type = cursor.fetchall()
        
        # Get certifications by issuing organization
        cursor.execute("""
            SELECT issuing_organization, COUNT(*) as count
            FROM certifications
            GROUP BY issuing_organization
            ORDER BY count DESC
            LIMIT 10
        """)
        by_organization = cursor.fetchall()
        
        # Get top students with most certifications
        cursor.execute("""
            SELECT s.id, s.name, s.registration_number, COUNT(c.id) as certification_count
            FROM students s
            JOIN certifications c ON s.id = c.student_id
            GROUP BY s.id, s.name, s.registration_number
            ORDER BY certification_count DESC
            LIMIT 5
        """)
        top_students = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            "total": total,
            "verified": verified,
            "by_type": by_type,
            "by_organization": by_organization,
            "top_students": top_students
        }
        
    except Exception as e:
        print(f"Error in get_certification_stats: {e}")
        traceback.print_exc()
        return {
            "total": 0,
            "verified": 0,
            "by_type": [],
            "by_organization": [],
            "top_students": []
        }