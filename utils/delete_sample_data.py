import mysql.connector
from database.db_config import DB_CONFIG

def delete_sample_data():
    """Delete all sample student and semester data for cleanup or reset."""

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # First delete from SemesterRecords (child table to avoid foreign key issues)
        cursor.execute("DELETE FROM SemesterRecords;")
        
        # Then delete from Students (parent table)
        cursor.execute("DELETE FROM Students;")
        
        conn.commit()
        print("🗑️  All sample data deleted successfully!")
    except mysql.connector.Error as err:
        print(f"❌ Error while deleting data: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    delete_sample_data()
