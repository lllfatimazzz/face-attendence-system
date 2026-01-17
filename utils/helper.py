"""Helper utility functions"""
import cv2
from datetime import datetime

def capture_frame(camera):
    """Capture a frame from the camera"""
    ret, frame = camera.read()
    if ret:
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return rgb_frame, frame
    return None, None

def resize_frame(frame, width=640):
    """Resize frame maintaining aspect ratio"""
    if frame is None:
        return None
    
    height = int(frame.shape[0] * width / frame.shape[1])
    return cv2.resize(frame, (width, height))

def draw_rectangle(frame, location, label=""):
    """Draw rectangle and label on frame"""
    top, right, bottom, left = location
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    if label:
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, label, (left + 6, bottom - 6), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    return frame

def format_datetime(dt=None):
    """Format datetime for display"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

