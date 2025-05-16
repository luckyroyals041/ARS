from database.mysql_data_handler import get_connection
import traceback

def get_student_achievements(student_id=None, verified_only=False):
    """Get achievements for a specific student or all achievements."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT a.*, s.name as student_name, s.registration_number, 
                   u.first_name as verifier_first_name, u.last_name as verifier_last_name
            FROM achievements a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN users u ON a.verified_by = u.id
            WHERE 1=1
        """
        params = []
        
        if student_id:
            query += " AND a.student_id = %s"
            params.append(student_id)
        
        if verified_only:
            query += " AND a.verified = TRUE"
        
        query += " ORDER BY a.achievement_date DESC"
        
        cursor.execute(query, params)
        achievements = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return achievements
        
    except Exception as e:
        print(f"Error in get_student_achievements: {e}")
        traceback.print_exc()
        return []

def get_achievement_by_id(achievement_id):
    """Get a specific achievement by ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT a.*, s.name as student_name, s.registration_number, 
                   u.first_name as verifier_first_name, u.last_name as verifier_last_name
            FROM achievements a
            JOIN students s ON a.student_id = s.id
            LEFT JOIN users u ON a.verified_by = u.id
            WHERE a.id = %s
        """
        
        cursor.execute(query, (achievement_id,))
        achievement = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return achievement
        
    except Exception as e:
        print(f"Error in get_achievement_by_id: {e}")
        traceback.print_exc()
        return None

def create_achievement(achievement_data):
    """Create a new achievement."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO achievements (
                student_id, title, description, achievement_type, 
                achievement_date, issuing_organization, certificate_url, verified
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            achievement_data['student_id'],
            achievement_data['title'],
            achievement_data.get('description', None),
            achievement_data['achievement_type'],
            achievement_data.get('achievement_date', None),
            achievement_data.get('issuing_organization', None),
            achievement_data.get('certificate_url', None),
            achievement_data.get('verified', False)
        ))
        
        achievement_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return achievement_id
        
    except Exception as e:
        print(f"Error in create_achievement: {e}")
        traceback.print_exc()
        return None

def update_achievement(achievement_id, achievement_data):
    """Update an existing achievement."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build the SET clause dynamically based on provided fields
        set_clause = []
        params = []
        
        for key, value in achievement_data.items():
            if key != 'id':  # Skip the ID field
                set_clause.append(f"{key} = %s")
                params.append(value)
        
        # Add the achievement_id to the parameters
        params.append(achievement_id)
        
        # Execute the update query
        cursor.execute(f"""
            UPDATE achievements
            SET {', '.join(set_clause)}
            WHERE id = %s
        """, params)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error in update_achievement: {e}")
        traceback.print_exc()
        return False

def verify_achievement(achievement_id, verified_by):
    """Verify an achievement."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE achievements
            SET verified = TRUE, verified_by = %s
            WHERE id = %s
        """
        
        cursor.execute(query, (verified_by, achievement_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error in verify_achievement: {e}")
        traceback.print_exc()
        return False

def delete_achievement(achievement_id):
    """Delete an achievement."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM achievements WHERE id = %s"
        
        cursor.execute(query, (achievement_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error in delete_achievement: {e}")
        traceback.print_exc()
        return False

def get_achievement_stats():
    """Get achievement statistics."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get total achievements count
        cursor.execute("SELECT COUNT(*) as total FROM achievements")
        total = cursor.fetchone()['total']
        
        # Get verified achievements count
        cursor.execute("SELECT COUNT(*) as verified FROM achievements WHERE verified = TRUE")
        verified = cursor.fetchone()['verified']
        
        # Get achievements by type
        cursor.execute("""
            SELECT achievement_type, COUNT(*) as count
            FROM achievements
            GROUP BY achievement_type
        """)
        by_type = cursor.fetchall()
        
        # Get top students with most achievements
        cursor.execute("""
            SELECT s.id, s.name, s.registration_number, COUNT(a.id) as achievement_count
            FROM students s
            JOIN achievements a ON s.id = a.student_id
            GROUP BY s.id, s.name, s.registration_number
            ORDER BY achievement_count DESC
            LIMIT 5
        """)
        top_students = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            "total": total,
            "verified": verified,
            "by_type": by_type,
            "top_students": top_students
        }
        
    except Exception as e:
        print(f"Error in get_achievement_stats: {e}")
        traceback.print_exc()
        return {
            "total": 0,
            "verified": 0,
            "by_type": [],
            "top_students": []
        }