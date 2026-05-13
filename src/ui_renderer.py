# ui_renderer.py
import numpy as np
import cv2

class UIRenderer:
    def __init__(self):
        self.landmark_color = (0, 255, 0) # Green inside
        self.landmark_border = (255, 255, 255) # White border
        self.landmark_radius = 8

    def draw(self, rgb_image, landmarks_dict, state_info=None):
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
                
        # Draw UI State Information
        if state_info:
            if state_info["is_completed"]:
                cv2.putText(annotated_image, "WORKOUT COMPLETE!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            else:
                text_y = 50
                cv2.putText(annotated_image, f"Exercise: {state_info['movement_name']}", (20, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                text_y += 40
                cv2.putText(annotated_image, f"Target Pose: {state_info['position_name']}", (20, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                
                text_y += 40
                cv2.putText(annotated_image, f"Reps: {state_info['current_reps']} / {state_info['target_reps']}", (20, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # Draw a simple hold progress bar
                bar_x = 20
                bar_y = text_y + 20
                bar_width = 300
                bar_height = 20
                progress = state_info['hold_progress']
                
                # Background
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
                # Foreground progress
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
                # Border
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 2)
                
                # Debug Info at bottom
                debug_info = state_info.get("debug_info", "")
                if debug_info:
                    cv2.putText(annotated_image, f"DEBUG: {debug_info}", (20, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
                    
                # Scale Factor at bottom
                scale_factor = state_info.get("scale_factor", 1.0)
                cv2.putText(annotated_image, f"SCALE: {scale_factor:.3f}", (20, h - 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
                
        return annotated_image