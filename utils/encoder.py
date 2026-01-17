"""Face encoding utilities"""
import pickle
import face_recognition
import numpy as np

def encode_face(image):
    """Encode a face image into a 128-dimensional vector"""
    try:
        # Convert to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 4:
            # RGBA to RGB
            image = image[:, :, :3]
        
        # Find face locations
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) == 0:
            return None
        
        # Get encodings for the face
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if len(face_encodings) > 0:
            return face_encodings[0]
        
        return None
    except Exception as e:
        print(f"Error encoding face: {e}")
        return None

def encode_to_bytes(face_encoding):
    """Convert numpy array to bytes for database storage"""
    if face_encoding is None:
        return None
    return pickle.dumps(face_encoding)

def bytes_to_encode(face_bytes):
    """Convert bytes from database back to numpy array"""
    if face_bytes is None:
        return None
    try:
        return pickle.loads(face_bytes)
    except Exception as e:
        print(f"Error decoding face encoding: {e}")
        return None

def compare_faces(encoding1, encoding2, tolerance=0.6):
    """Compare two face encodings"""
    if encoding1 is None or encoding2 is None:
        return False
    distance = face_recognition.face_distance([encoding1], encoding2)[0]
    return distance <= tolerance

