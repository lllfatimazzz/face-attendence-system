"""Main window for Face Attendance System"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from gui.register_window import RegisterWindow
from gui.attendance_window import AttendanceWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition Attendance System")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title = QLabel("Face Recognition Attendance System")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin: 20px;")
        main_layout.addWidget(title)
        
        # Button layout
        button_layout = QVBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(50, 30, 50, 30)
        
        # Register button
        self.register_btn = QPushButton("Register Face")
        self.register_btn.setMinimumHeight(60)
        self.register_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.register_btn.clicked.connect(self.open_register_window)
        button_layout.addWidget(self.register_btn)
        
        # Attendance button
        self.attendance_btn = QPushButton("Mark Attendance")
        self.attendance_btn.setMinimumHeight(60)
        self.attendance_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.attendance_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
        """)
        self.attendance_btn.clicked.connect(self.open_attendance_window)
        button_layout.addWidget(self.attendance_btn)
        
        # History button
        self.history_btn = QPushButton("View Attendance History")
        self.history_btn.setMinimumHeight(60)
        self.history_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.history_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #7d3c98;
            }
        """)
        self.history_btn.clicked.connect(self.open_history_window)
        button_layout.addWidget(self.history_btn)
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)
    
    def open_register_window(self):
        """Open registration window"""
        self.register_window = RegisterWindow()
        self.register_window.show()
    
    def open_attendance_window(self):
        """Open attendance window"""
        self.attendance_window = AttendanceWindow()
        self.attendance_window.show()
    
    def open_history_window(self):
        """Open history window"""
        self.history_window = AttendanceWindow(show_history=True)
        self.history_window.show()

