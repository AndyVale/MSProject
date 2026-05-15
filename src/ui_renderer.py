# ui_renderer.py
import numpy as np
import cv2

class UIRenderer:
    def __init__(self):
        self.landmark_color = (0, 255, 0) # Green inside
        self.landmark_border = (255, 255, 255) # White border
        self.landmark_radius = 8
        self._image_cache = {}

    def _get_image(self, path):
        if path not in self._image_cache:
            img = cv2.imread(path)
            if img is not None:
                self._image_cache[path] = img
            else:
                return None
        return self._image_cache[path]

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
                text_y = 80
                
                def draw_text_with_bg(img, text, position, font_scale, text_color, bg_color, thickness=3):
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
                    x, y = position
                    cv2.rectangle(img, (x, y - text_h - 10), (x + text_w + 10, y + baseline + 10), bg_color, -1)
                    cv2.putText(img, text, (x + 5, y), font, font_scale, text_color, thickness)
                    return y + baseline + 10

                text_y = draw_text_with_bg(annotated_image, f"Exercise: {state_info['movement_name']}", (20, text_y), 1.5, (255, 255, 255), (0, 0, 0)) + 20
                text_y = draw_text_with_bg(annotated_image, f"Target: {state_info['position_name']}", (20, text_y), 1.5, (255, 255, 0), (0, 0, 0)) + 20
                text_y = draw_text_with_bg(annotated_image, f"Reps: {state_info['current_reps']} / {state_info['target_reps']}", (20, text_y), 1.5, (0, 255, 255), (0, 0, 0)) + 40
                
                # Draw Pose Image
                pose_path = state_info.get("pose_image_path")
                if pose_path:
                    pose_img = self._get_image(pose_path)
                    if pose_img is not None:
                        # Resize pose image to fit in the UI (e.g., 200px width)
                        target_w = 300
                        aspect_ratio = pose_img.shape[0] / pose_img.shape[1]
                        target_h = int(target_w * aspect_ratio)
                        pose_img_resized = cv2.resize(pose_img, (target_w, target_h))
                        
                        # Place in top right corner
                        margin = 20
                        start_x = w - target_w - margin
                        start_y = margin
                        
                        # Draw a border around the pose image
                        cv2.rectangle(annotated_image, (start_x - 5, start_y - 5), (start_x + target_w + 5, start_y + target_h + 5), (255, 255, 255), -1)
                        annotated_image[start_y:start_y+target_h, start_x:start_x+target_w] = pose_img_resized

                # Draw a massive hold progress bar
                bar_x = 20
                bar_y = text_y
                bar_width = 400
                bar_height = 40
                progress = state_info['hold_progress']
                
                # Background
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
                # Foreground progress
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
                # Border
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 3)
                
                # Debug Info at bottom
                debug_info = state_info.get("debug_info", "")
                if debug_info:
                    cv2.putText(annotated_image, f"DEBUG: {debug_info}", (20, h - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
                    
                # Scale Factor at bottom
                scale_factor = state_info.get("scale_factor", 1.0)
                cv2.putText(annotated_image, f"SCALE: {scale_factor:.3f}", (20, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
                
        return annotated_image