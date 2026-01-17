"""Attendance window for marking attendance and viewing history"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QDateEdit, QComboBox)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QImage, QPixmap
import cv2
from datetime import datetime
from core.attendance import AttendanceTracker
from core.face_recognition import FaceRecognizer

class AttendanceWindow(QWidget):
    def __init__(self, show_history=False):
        super().__init__()
        self.show_history_mode = show_history
        self.camera = None
        self.attendance_tracker = AttendanceTracker()
        self.face_recognizer = FaceRecognizer()
        self.last_recognized = None
        self.last_attendance_time = None
        
        if show_history:
            self.setWindowTitle("Attendance History")
            self.setGeometry(150, 150, 1000, 600)
        else:
            self.setWindowTitle("Mark Attendance")
            self.setGeometry(150, 150, 900, 700)
        
        self.init_ui()
        
        if not show_history:
            self.start_camera()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        if self.show_history_mode:
            self.init_history_ui(layout)
        else:
            self.init_attendance_ui(layout)
        
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def init_attendance_ui(self, layout):
        """Initialize attendance marking UI"""
        # Title
        title = QLabel("Mark Attendance")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(title)
        
        # Video display
        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("border: 2px solid #34495e; background-color: #2c3e50;")
        self.video_label.setText("Initializing camera...")
        layout.addWidget(self.video_label)
        
        # Status label
        self.status_label = QLabel("Position your face in front of the camera")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setStyleSheet("color: #27ae60; margin: 10px; padding: 10px; background-color: white; border-radius: 5px;")
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.mark_btn = QPushButton("Mark Attendance")
        self.mark_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.mark_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.mark_btn.clicked.connect(self.mark_attendance)
        button_layout.addWidget(self.mark_btn)
        
        self.history_btn = QPushButton("View History")
        self.history_btn.setFont(QFont("Arial", 12))
        self.history_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.history_btn.clicked.connect(self.show_history)
        button_layout.addWidget(self.history_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.setFont(QFont("Arial", 12))
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # Timer for video updates and auto-attendance
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # Update every 100ms
    
    def init_history_ui(self, layout):
        """Initialize history viewing UI"""
        # Title
        title = QLabel("Attendance History")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(title)
        
        # Filter layout
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Filter by Date:"))
        self.date_filter = QDateEdit()
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setCalendarPopup(True)
        self.date_filter.dateChanged.connect(self.refresh_history)
        filter_layout.addWidget(self.date_filter)
        
        filter_layout.addWidget(QLabel("Filter by Role:"))
        self.role_filter = QComboBox()
        self.role_filter.addItems(["All", "Student", "Teacher"])
        self.role_filter.currentTextChanged.connect(self.refresh_history)
        filter_layout.addWidget(self.role_filter)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_history)
        filter_layout.addWidget(refresh_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "User ID", "Name", "Role", "Branch/Designation", "Date", "Time", "Timestamp"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFont(QFont("Arial", 10))
        layout.addWidget(self.table)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        layout.addWidget(close_btn)
        
        self.refresh_history()
    
    def start_camera(self):
        """Start the camera"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                QMessageBox.critical(self, "Error", "Could not open camera")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Camera error: {str(e)}")
    
    def update_frame(self):
        """Update video frame and recognize faces"""
        if self.camera is None:
            return
        
        ret, frame = self.camera.read()
        if not ret:
            return
        
        # Recognize face
        user_info = self.face_recognizer.recognize_face(frame)
        
        if user_info:
            # Draw rectangle and label
            top, right, bottom, left = user_info['location']
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            label = f"{user_info['name']} ({user_info['user_id']})"
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            # Update status
            branch_designation = user_info.get('branch') or user_info.get('designation', 'N/A')
            self.status_label.setText(
                f"Recognized: {user_info['name']} | ID: {user_info['user_id']} | "
                f"Role: {user_info['role'].capitalize()} | {branch_designation}"
            )
            self.status_label.setStyleSheet("color: #27ae60; margin: 10px; padding: 10px; background-color: white; border-radius: 5px;")
            
            self.last_recognized = user_info
        else:
            self.status_label.setText("No face recognized. Position your face in front of the camera.")
            self.status_label.setStyleSheet("color: #e74c3c; margin: 10px; padding: 10px; background-color: white; border-radius: 5px;")
        
        # Convert to QImage
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap.scaled(
            self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
    
    def mark_attendance(self):
        """Mark attendance for recognized user"""
        if self.last_recognized is None:
            QMessageBox.warning(self, "Error", "No face recognized. Please position your face in front of the camera.")
            return
        
        # Prevent duplicate attendance within 1 minute
        current_time = datetime.now()
        if (self.last_attendance_time and 
            (current_time - self.last_attendance_time).seconds < 60 and
            self.last_recognized['user_id'] == self.last_recognized.get('last_marked_id')):
            QMessageBox.information(self, "Info", "Attendance already marked recently. Please wait.")
            return
        
        user_info = self.last_recognized
        success = self.attendance_tracker.mark_attendance(
            user_info['user_id'],
            user_info['name'],
            user_info['role'],
            user_info.get('branch'),
            user_info.get('designation')
        )
        
        if success:
            QMessageBox.information(
                self, "Success",
                f"Attendance marked successfully for {user_info['name']}!"
            )
            self.last_attendance_time = current_time
            self.last_recognized['last_marked_id'] = user_info['user_id']
        else:
            QMessageBox.warning(self, "Error", "Failed to mark attendance")
    
    def show_history(self):
        """Open history window"""
        self.history_window = AttendanceWindow(show_history=True)
        self.history_window.show()
    
    def refresh_history(self):
        """Refresh attendance history table"""
        if not self.show_history_mode:
            return
        
        # Get selected date
        selected_date = self.date_filter.date().toPyDate()
        records = self.attendance_tracker.get_attendance_history(date=selected_date)
        
        # Filter by role if needed
        role_filter = self.role_filter.currentText()
        if role_filter != "All":
            records = [r for r in records if r['role'].lower() == role_filter.lower()]
        
        # Populate table
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(record['user_id']))
            self.table.setItem(row, 1, QTableWidgetItem(record['name']))
            self.table.setItem(row, 2, QTableWidgetItem(record['role'].capitalize()))
            
            branch_designation = record.get('branch') or record.get('designation', 'N/A')
            self.table.setItem(row, 3, QTableWidgetItem(branch_designation))
            self.table.setItem(row, 4, QTableWidgetItem(str(record['date'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(record['time'])))
            self.table.setItem(row, 6, QTableWidgetItem(str(record.get('timestamp', 'N/A'))))
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.camera is not None:
            self.camera.release()
        event.accept()

