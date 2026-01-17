"""Core face recognition functionality"""
import cv2
import face_recognition
import numpy as np
from utils.encoder import bytes_to_encode, compare_faces
from database.db_queries import DatabaseQueries

class FaceRecognizer:
    def __init__(self):
        self.db_queries = DatabaseQueries()
        self.known_face_encodings = []
        self.known_face_ids = []
        self.known_face_names = []
        self.known_face_roles = []
        self.known_face_branches = []
        self.known_face_designations = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load all known faces from database"""
        users = self.db_queries.get_all_users()
        self.known_face_encodings = []
        self.known_face_ids = []
        self.known_face_names = []
        self.known_face_roles = []
        self.known_face_branches = []
        self.known_face_designations = []
        
        for user in users:
            face_encoding = bytes_to_encode(user['face_encoding'])
            if face_encoding is not None:
                self.known_face_encodings.append(face_encoding)
                self.known_face_ids.append(user['user_id'])
                self.known_face_names.append(user['name'])
                self.known_face_roles.append(user['role'])
                self.known_face_branches.append(user.get('branch', ''))
                self.known_face_designations.append(user.get('designation', ''))
    
    def recognize_face(self, frame, tolerance=0.6):
        """Recognize face in frame and return user info"""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find face locations
        face_locations = face_recognition.face_locations(rgb_small_frame)
        
        if len(face_locations) == 0:
            return None
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        if len(face_encodings) == 0:
            return None
        
        # Scale back up face locations
        face_locations = [(top*4, right*4, bottom*4, left*4) 
                         for (top, right, bottom, left) in face_locations]
        
        # Compare with known faces
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding, tolerance=tolerance
            )
            
            if True in matches:
                match_index = matches.index(True)
                return {
                    'user_id': self.known_face_ids[match_index],
                    'name': self.known_face_names[match_index],
                    'role': self.known_face_roles[match_index],
                    'branch': self.known_face_branches[match_index],
                    'designation': self.known_face_designations[match_index],
                    'location': face_location,
                    'encoding': face_encoding
                }
        
        return None
    
    def refresh_database(self):
        """Refresh known faces from database"""
        self.load_known_faces()

