# pose_extractor.py
import mediapipe as mp
from mediapipe.tasks.python import vision

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
            if idx == -1: # Custom Center of Gravity (CG)
                left_hip = pose[23]
                right_hip = pose[24]
                landmarks_dict[-1] = {
                    "x": (left_hip.x + right_hip.x) / 2.0,
                    "y": (left_hip.y + right_hip.y) / 2.0,
                    "z": (left_hip.z + right_hip.z) / 2.0
                }
            elif 0 <= idx < len(pose):
                landmark = pose[idx]
                landmarks_dict[idx] = {
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z
                }
                
        return landmarks_dict