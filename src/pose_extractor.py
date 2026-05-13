# pose_extractor.py
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import vision
from utils.constants import CG_INDEX

# Approximate mass distribution weights for the 33 landmarks
_RAW_WEIGHTS = np.array([
    # 0-10: Head/Face
    1.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.5, 0.5, 0.2, 0.2,
    # 11-12: Shoulders (upper trunk)
    5.0, 5.0,
    # 13-16: Arms
    1.5, 1.5, 1.0, 1.0,
    # 17-22: Hands
    0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
    # 23-24: Hips (lower trunk)
    10.0, 10.0,
    # 25-26: Knees
    4.0, 4.0,
    # 27-32: Ankles/Feet
    1.5, 1.5, 1.0, 1.0, 0.5, 0.5
])
NORMALIZED_WEIGHTS = _RAW_WEIGHTS / np.sum(_RAW_WEIGHTS)

class PoseExtractor:
    def __init__(self, required_landmarks=None):
        self.latest_raw_result = None
        self.latest_result = None
        self.latest_image = None
        self.required_landmarks = required_landmarks if required_landmarks else []

    def process_result(self, result: vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.latest_raw_result = result
        self.latest_result = self.get_landmarks_dict(result)
        self.latest_image = output_image.numpy_view()
        
    def get_landmarks_dict(self, result: vision.PoseLandmarkerResult) -> dict:
        """
        Extracts the landmarks from the result and returns them as a dictionary.
        """
        landmarks_dict = {}
        if not result or not result.pose_landmarks:
            return landmarks_dict
            
        # Assuming a single person in frame, using the first detected pose
        pose = result.pose_landmarks[0]
        
        for idx in self.required_landmarks:
            if idx == CG_INDEX: # Custom Center of Gravity (CG)
                # Compute weighted sum of all 33 landmarks
                cg_x = 0.0
                cg_y = 0.0
                cg_z = 0.0
                
                for i in range(len(pose)):
                    weight = NORMALIZED_WEIGHTS[i]
                    cg_x += pose[i].x * weight
                    cg_y += pose[i].y * weight
                    cg_z += pose[i].z * weight
                    
                landmarks_dict[CG_INDEX] = {
                    "x": cg_x,
                    "y": cg_y,
                    "z": cg_z
                }
            elif 0 <= idx < len(pose):
                landmark = pose[idx]
                landmarks_dict[idx] = {
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z
                }
                
        return landmarks_dict