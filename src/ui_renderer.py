# ui_renderer.py
import numpy as np
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python import vision

class UIRenderer:
    def __init__(self):
        self.pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
        self.pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

    def draw(self, rgb_image, detection_result):
        # If there's no image or no detection yet, just return the raw image
        if rgb_image is None:
            return None
            
        annotated_image = np.copy(rgb_image)

        if detection_result and detection_result.pose_landmarks:
            pose_landmarks_list = detection_result.pose_landmarks
            for pose_landmarks in pose_landmarks_list:
                drawing_utils.draw_landmarks(
                    image=annotated_image,
                    landmark_list=pose_landmarks,
                    connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
                    landmark_drawing_spec=self.pose_landmark_style,
                    connection_drawing_spec=self.pose_connection_style)
        return annotated_image