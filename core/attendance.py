"""Attendance tracking module"""
from datetime import datetime
from database.db_queries import DatabaseQueries

class AttendanceTracker:
    def __init__(self):
        self.db_queries = DatabaseQueries()
    
    def mark_attendance(self, user_id, name, role, branch=None, designation=None):
        """Mark attendance for a recognized user"""
        return self.db_queries.mark_attendance(user_id, name, role, branch, designation)
    
    def get_attendance_history(self, user_id=None, date=None):
        """Get attendance history"""
        return self.db_queries.get_attendance_history(user_id, date)
    
    def format_attendance_record(self, record):
        """Format attendance record for display"""
        return {
            'id': record['user_id'],
            'name': record['name'],
            'role': record['role'].capitalize(),
            'branch': record.get('branch', 'N/A'),
            'designation': record.get('designation', 'N/A'),
            'date': str(record['date']),
            'time': str(record['time'])
        }

