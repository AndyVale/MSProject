# pose_extractor.py
import mediapipe as mp
from mediapipe.tasks.python import vision

class PoseExtractor:
    def __init__(self):
        self.latest_result = None
        self.latest_image = None

    def process_result(self, result: vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.latest_result = result
        self.latest_image = output_image.numpy_view()
        
    def get_landmarks_dict(self):
        """
        Later, you can add a method here that converts self.latest_result
        into a clean dictionary of x,y coordinates (like extracting 
        just the ankles, hips, and calculating the Center of Gravity)
        to send to your exercise_evaluator.
        """
        pass