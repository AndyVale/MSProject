# ui_renderer.py
import numpy as np
import cv2

class UIRenderer:
    def __init__(self):
        self.landmark_color = (0, 255, 0) # Green inside
        self.landmark_border = (255, 255, 255) # White border
        self.landmark_radius = 8

    def draw(self, rgb_image, landmarks_dict):
        # If there's no image, just return None
        if rgb_image is None:
            return None
            
        annotated_image = np.copy(rgb_image)
        h, w, _ = annotated_image.shape

        if landmarks_dict:
            for idx, landmark in landmarks_dict.items():
                x = int(landmark["x"] * w)
                y = int(landmark["y"] * h)
                
                # Draw white border
                cv2.circle(annotated_image, (x, y), self.landmark_radius + 2, self.landmark_border, -1)
                # Draw green center
                cv2.circle(annotated_image, (x, y), self.landmark_radius, self.landmark_color, -1)
                
        return annotated_image