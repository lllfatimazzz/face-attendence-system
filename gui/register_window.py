"""Registration window for face registration"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox, QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QImage, QPixmap
import cv2
import numpy as np
import face_recognition
from core.register import Registration
from core.face_recognition import FaceRecognizer

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Registration")
        self.setGeometry(150, 150, 900, 700)
        self.camera = None
        self.registration = Registration()
        self.face_recognizer = FaceRecognizer()
        self.init_ui()
        self.start_camera()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("Register New Face")
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
        
        # Form layout
        form_layout = QVBoxLayout()
        
        # Role selection
        role_layout = QHBoxLayout()
        role_label = QLabel("Role:")
        role_label.setFont(QFont("Arial", 11))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["student", "teacher"])
        self.role_combo.setFont(QFont("Arial", 11))
        self.role_combo.currentTextChanged.connect(self.on_role_changed)
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        role_layout.addStretch()
        form_layout.addLayout(role_layout)
        
        # User ID
        id_layout = QHBoxLayout()
        id_label = QLabel("User ID:")
        id_label.setFont(QFont("Arial", 11))
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Enter unique user ID")
        self.user_id_input.setFont(QFont("Arial", 11))
        id_layout.addWidget(id_label)
        id_layout.addWidget(self.user_id_input)
        form_layout.addLayout(id_layout)
        
        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setFont(QFont("Arial", 11))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")
        self.name_input.setFont(QFont("Arial", 11))
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)
        
        # Branch/Designation
        self.branch_layout = QHBoxLayout()
        self.branch_label = QLabel("Branch:")
        self.branch_label.setFont(QFont("Arial", 11))
        self.branch_input = QLineEdit()
        self.branch_input.setPlaceholderText("Enter branch (for students)")
        self.branch_input.setFont(QFont("Arial", 11))
        self.branch_layout.addWidget(self.branch_label)
        self.branch_layout.addWidget(self.branch_input)
        form_layout.addLayout(self.branch_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.capture_btn = QPushButton("Capture & Register")
        self.capture_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.capture_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.capture_btn.clicked.connect(self.capture_and_register)
        button_layout.addWidget(self.capture_btn)
        
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
        
        # Status label
        self.status_label = QLabel("Position your face in front of the camera")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #7f8c8d; margin: 10px;")
        layout.addWidget(self.status_label)
        
        # Timer for video updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms
        
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def on_role_changed(self, role):
        """Handle role change"""
        if role == "student":
            self.branch_label.setText("Branch:")
            self.branch_input.setPlaceholderText("Enter branch (for students)")
        else:
            self.branch_label.setText("Designation:")
            self.branch_input.setPlaceholderText("Enter designation (for teachers)")
    
    def start_camera(self):
        """Start the camera"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                QMessageBox.critical(self, "Error", "Could not open camera")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Camera error: {str(e)}")
    
    def update_frame(self):
        """Update video frame"""
        if self.camera is None:
            return
        
        ret, frame = self.camera.read()
        if ret:
            # Detect face and draw rectangle
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = self.detect_face(rgb_frame)
            
            if face_locations:
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (left, top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Convert to QImage
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap.scaled(
                self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
    
    def detect_face(self, frame):
        """Detect face in frame"""
        face_locations = face_recognition.face_locations(frame)
        if len(face_locations) > 0:
            # Scale back (if frame was resized)
            return face_locations[0]
        return None
    
    def capture_and_register(self):
        """Capture frame and register user"""
        if self.camera is None:
            QMessageBox.warning(self, "Error", "Camera not available")
            return
        
        # Validate inputs
        user_id = self.user_id_input.text().strip()
        name = self.name_input.text().strip()
        role = self.role_combo.currentText()
        branch = self.branch_input.text().strip() if role == "student" else None
        designation = self.branch_input.text().strip() if role == "teacher" else None
        
        if not user_id or not name:
            QMessageBox.warning(self, "Validation Error", "Please fill in User ID and Name")
            return
        
        if role == "student" and not branch:
            QMessageBox.warning(self, "Validation Error", "Please enter branch for students")
            return
        
        if role == "teacher" and not designation:
            QMessageBox.warning(self, "Validation Error", "Please enter designation for teachers")
            return
        
        # Capture frame
        ret, frame = self.camera.read()
        if not ret:
            QMessageBox.warning(self, "Error", "Failed to capture frame")
            return
        
        # Register
        success, message = self.registration.capture_and_register(
            frame, user_id, name, role, branch, designation
        )
        
        if success:
            QMessageBox.information(self, "Success", message)
            # Refresh face recognizer
            self.face_recognizer.refresh_database()
            # Clear inputs
            self.user_id_input.clear()
            self.name_input.clear()
            self.branch_input.clear()
        else:
            QMessageBox.warning(self, "Registration Failed", message)
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.camera is not None:
            self.camera.release()
        event.accept()

