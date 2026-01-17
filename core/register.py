"""Registration module for face attendance system"""
import cv2
import face_recognition
from utils.encoder import encode_face, encode_to_bytes
from database.db_queries import DatabaseQueries

class Registration:
    def __init__(self):
        self.db_queries = DatabaseQueries()
    
    def capture_and_register(self, frame, user_id, name, role, branch=None, designation=None):
        """Capture face from frame and register user"""
        try:
            # Convert BGR to RGB if needed
            if len(frame.shape) == 3:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                rgb_frame = frame
            
            # Encode face
            face_encoding = encode_face(rgb_frame)
            
            if face_encoding is None:
                return False, "No face detected in the image"
            
            # Convert to bytes
            face_encoding_bytes = encode_to_bytes(face_encoding)
            
            # Check if user already exists
            existing_user = self.db_queries.get_user_by_id(user_id)
            if existing_user:
                # Update existing user
                success = self.db_queries.update_face_encoding(user_id, face_encoding_bytes)
                if success:
                    return True, "Face updated successfully"
                else:
                    return False, "Failed to update face encoding"
            else:
                # Add new user
                success = self.db_queries.add_user(
                    user_id, name, role, branch, designation, face_encoding_bytes
                )
                if success:
                    return True, "Registration successful"
                else:
                    return False, "Failed to register user"
        except Exception as e:
            return False, f"Error during registration: {str(e)}"
    
    def validate_user_id(self, user_id):
        """Validate if user_id already exists"""
        user = self.db_queries.get_user_by_id(user_id)
        return user is not None

