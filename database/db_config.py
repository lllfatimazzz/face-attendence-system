"""Database configuration for Face Attendance System"""
import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'face_attendance_db'
        self.user = 'root'
        self.password = 'root'  # Change this to your MySQL password
        
    def get_connection(self):
        """Create and return database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def initialize_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            # First connect without database to create it
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            connection.close()
            
            # Now connect to the database
            connection = self.get_connection()
            if connection:
                cursor = connection.cursor()
                
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(50) UNIQUE NOT NULL,
                        name VARCHAR(100) NOT NULL,
                        role ENUM('student', 'teacher') NOT NULL,
                        branch VARCHAR(100),
                        designation VARCHAR(100),
                        face_encoding BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create attendance table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS attendance (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id VARCHAR(50) NOT NULL,
                        name VARCHAR(100) NOT NULL,
                        role ENUM('student', 'teacher') NOT NULL,
                        branch VARCHAR(100),
                        designation VARCHAR(100),
                        date DATE NOT NULL,
                        time TIME NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """)
                
                connection.commit()
                cursor.close()
                connection.close()
                print("Database initialized successfully")
                return True
        except Error as e:
            print(f"Error initializing database: {e}")
            return False

