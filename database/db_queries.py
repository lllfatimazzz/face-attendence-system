"""Database queries for Face Attendance System"""
import mysql.connector
from datetime import datetime
from database.db_config import DatabaseConfig

class DatabaseQueries:
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def add_user(self, user_id, name, role, branch=None, designation=None, face_encoding=None):
        """Add a new user to the database"""
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO users (user_id, name, role, branch, designation, face_encoding)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (user_id, name, role, branch, designation, face_encoding)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error adding user: {e}")
            if connection:
                connection.close()
            return False
    
    def update_face_encoding(self, user_id, face_encoding):
        """Update face encoding for a user"""
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "UPDATE users SET face_encoding = %s WHERE user_id = %s"
            cursor.execute(query, (face_encoding, user_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error updating face encoding: {e}")
            if connection:
                connection.close()
            return False
    
    def get_all_users(self):
        """Get all users with their face encodings"""
        connection = self.db_config.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE face_encoding IS NOT NULL")
            users = cursor.fetchall()
            cursor.close()
            connection.close()
            return users
        except Error as e:
            print(f"Error getting users: {e}")
            if connection:
                connection.close()
            return []
    
    def get_user_by_id(self, user_id):
        """Get user by user_id"""
        connection = self.db_config.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            if connection:
                connection.close()
            return None
    
    def mark_attendance(self, user_id, name, role, branch=None, designation=None):
        """Mark attendance for a user"""
        connection = self.db_config.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            now = datetime.now()
            query = """
                INSERT INTO attendance (user_id, name, role, branch, designation, date, time)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (user_id, name, role, branch, designation, now.date(), now.time())
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error marking attendance: {e}")
            if connection:
                connection.close()
            return False
    
    def get_attendance_history(self, user_id=None, date=None):
        """Get attendance history, optionally filtered by user_id or date"""
        connection = self.db_config.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            if user_id:
                query = "SELECT * FROM attendance WHERE user_id = %s ORDER BY timestamp DESC"
                cursor.execute(query, (user_id,))
            elif date:
                query = "SELECT * FROM attendance WHERE date = %s ORDER BY timestamp DESC"
                cursor.execute(query, (date,))
            else:
                query = "SELECT * FROM attendance ORDER BY timestamp DESC"
                cursor.execute(query)
            
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
        except Error as e:
            print(f"Error getting attendance history: {e}")
            if connection:
                connection.close()
            return []

