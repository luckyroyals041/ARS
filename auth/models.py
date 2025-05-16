import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from database.mysql_data_handler import get_connection

def create_users_table():
    """Create the users table if it doesn't exist."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                role ENUM('faculty', 'hod', 'principal') NOT NULL,
                department VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        
        # Check if admin user exists, if not create one
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        admin_exists = cursor.fetchone()
        
        if not admin_exists:
            # Create default admin user (principal role)
            cursor.execute("""
                INSERT INTO users (username, password_hash, email, first_name, last_name, role, department)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                'admin',
                generate_password_hash('admin123'),
                'admin@example.com',
                'Admin',
                'User',
                'principal',
                'Administration'
            ))
            
            conn.commit()
            print("✅ Default admin user created")
        
        cursor.close()
        conn.close()
        
        print("✅ Users table created or already exists")
        return True
        
    except Exception as e:
        print(f"❌ Error creating users table: {e}")
        return False

def get_user_by_username(username):
    """Get user by username."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM users WHERE username = %s
        """, (username,))
        
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
        
    except Exception as e:
        print(f"Error in get_user_by_username: {e}")
        return None

def get_user_by_id(user_id):
    """Get user by ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM users WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
        
    except Exception as e:
        print(f"Error in get_user_by_id: {e}")
        return None

def create_user(user_data):
    """Create a new user."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (
                username, password_hash, email, first_name, last_name, 
                role, department, is_active
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_data['username'],
            user_data['password_hash'],
            user_data['email'],
            user_data['first_name'],
            user_data['last_name'],
            user_data['role'],
            user_data.get('department', None),
            user_data.get('is_active', True)
        ))
        
        user_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return user_id
        
    except Exception as e:
        print(f"Error in create_user: {e}")
        return None

def update_user(user_id, user_data):
    """Update an existing user."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build the SET clause dynamically based on provided fields
        set_clause = []
        params = []
        
        for key, value in user_data.items():
            if key != 'id':  # Skip the ID field
                set_clause.append(f"{key} = %s")
                params.append(value)
        
        # Add the user_id to the parameters
        params.append(user_id)
        
        # Execute the update query
        cursor.execute(f"""
            UPDATE users
            SET {', '.join(set_clause)}
            WHERE id = %s
        """, params)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error in update_user: {e}")
        return False

def verify_password(user, password):
    """Verify a user's password."""
    if not user or not password:
        return False
    
    return check_password_hash(user['password_hash'], password)

def get_users_by_role(role=None, department=None):
    """Get users by role and optionally by department."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM users WHERE 1=1"
        params = []
        
        if role:
            query += " AND role = %s"
            params.append(role)
        
        if department:
            query += " AND department = %s"
            params.append(department)
        
        cursor.execute(query, params)
        
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return users
        
    except Exception as e:
        print(f"Error in get_users_by_role: {e}")
        return []

def get_all_users():
    """Get all users."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users")
        
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return users
        
    except Exception as e:
        print(f"Error in get_all_users: {e}")
        return []