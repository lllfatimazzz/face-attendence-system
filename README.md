# face-attendence-system
# Face Recognition Attendance System

A modern face recognition attendance system built with PyQt5, featuring separate interfaces for students and teachers, automatic face registration via webcam, and comprehensive attendance tracking.

## Features

- **Face Registration**: Register users using webcam without manual image upload
- **Role-based System**: Separate interfaces for students and teachers
- **MySQL Database**: Secure storage of user data and face encodings
- **Attendance Tracking**: Automatic attendance marking with face recognition
- **History Viewing**: View attendance logs with filtering options
- **Modern GUI**: Beautiful PyQt5 interface with intuitive controls

## Requirements

- Python 3.7+
- MySQL Server
- Webcam

## Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

**Note**: Installing `dlib` might require additional setup:
- On Windows, you may need to install Visual C++ Build Tools
- On Linux/Mac, you may need CMake and other dependencies

3. Configure MySQL database:
   - Make sure MySQL server is running
   - Update database credentials in `database/db_config.py`:
     ```python
     self.host = 'localhost'
     self.database = 'face_attendance_db'
     self.user = 'root'
     self.password = 'your_password'  # Change this
     ```

4. Run the application:
```bash
python main.py
```

## Usage

### Registering a User

1. Click "Register Face" from the main window
2. Select role (Student or Teacher)
3. Enter User ID, Name, and Branch (for students) or Designation (for teachers)
4. Position your face in front of the webcam
5. Click "Capture & Register"

### Marking Attendance

1. Click "Mark Attendance" from the main window
2. Position your face in front of the webcam
3. The system will recognize your face automatically
4. Click "Mark Attendance" button to record attendance

### Viewing History

1. Click "View Attendance History" from the main window
2. Use filters to view attendance by date or role
3. All records show: User ID, Name, Role, Branch/Designation, Date, and Time

## Project Structure

```
Face_Attendance_System/
├── gui/                        # PyQt5 GUI components
│   ├── main_window.py          # Main window with navigation
│   ├── register_window.py      # Face registration interface
│   └── attendance_window.py    # Attendance marking and history
├── core/                       # Core logic
│   ├── face_recognition.py     # Face recognition engine
│   ├── attendance.py           # Attendance tracking
│   └── register.py             # User registration
├── database/
│   ├── db_config.py            # Database configuration
│   └── db_queries.py           # Database queries
├── utils/
│   ├── encoder.py              # Face encoding utilities
│   └── helper.py               # Helper functions
├── assets/                     # Icons, logos (optional)
├── main.py                     # Application entry point
└── requirements.txt            # Python dependencies
```

## Database Schema

### Users Table
- `id`: Primary key
- `user_id`: Unique user identifier
- `name`: User's full name
- `role`: 'student' or 'teacher'
- `branch`: Branch (for students)
- `designation`: Designation (for teachers)
- `face_encoding`: BLOB storing face encoding
- `created_at`: Registration timestamp

### Attendance Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `name`: User's name
- `role`: User's role
- `branch`: Branch/Designation
- `designation`: Designation (if teacher)
- `date`: Attendance date
- `time`: Attendance time
- `timestamp`: Full timestamp

## Troubleshooting

1. **Camera not working**: Make sure no other application is using the webcam
2. **Database connection error**: Verify MySQL is running and credentials are correct
3. **Face not recognized**: Ensure good lighting and face is clearly visible
4. **dlib installation issues**: 
   - Windows: Install Visual C++ Build Tools
   - Linux: `sudo apt-get install cmake libopenblas-dev liblapack-dev`
   - Mac: `brew install cmake`

## License

This project is open source and available for educational purposes.

## Notes

- The system prevents duplicate attendance within 1 minute for the same user
- Face encodings are stored as binary data in MySQL
- Make sure to have good lighting conditions for better face recognition accuracy
