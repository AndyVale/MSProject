# ui_renderer.py
import numpy as np
import cv2
import subprocess
from utils.constants import SCREEN_1280x720

class UIRenderer:
    def __init__(self):
        self.landmark_color = (0, 255, 0) # Green inside
        self.landmark_border = (255, 255, 255) # White border
        self.landmark_radius = 8
        self._image_cache = {}
        self._workout_completed_sound_played = False

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
            base_scale = w / float(SCREEN_1280x720[0])
            radius = max(2, int(self.landmark_radius * base_scale))
            for idx, landmark in landmarks_dict.items():
                x = int(landmark["x"] * w)
                y = int(landmark["y"] * h)
                
                # Draw white border
                cv2.circle(annotated_image, (x, y), radius + max(1, int(2 * base_scale)), self.landmark_border, -1)
                # Draw green center
                cv2.circle(annotated_image, (x, y), radius, self.landmark_color, -1)
                
        # Draw UI State Information
        if state_info:
            base_scale = w / float(SCREEN_1280x720[0])
            if state_info["is_completed"]:
                font_scale_large = 1.5 * base_scale
                thickness_large = max(2, int(3 * base_scale))
                cv2.putText(annotated_image, "WORKOUT COMPLETE!", (int(w * 0.05), int(h * 0.1)), cv2.FONT_HERSHEY_SIMPLEX, font_scale_large, (0, 255, 0), thickness_large)
                if not self._workout_completed_sound_played: # to avoid replaying the sound in loop
                    subprocess.Popen(["gst-play-1.0", "exercises/end_workout.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self._workout_completed_sound_played = True
            else:
                text_y = int(h * 0.08)
                font_scale = 1.5 * base_scale
                thickness = max(2, int(3 * base_scale))
                margin_x = int(w * 0.02)
                padding = int(10 * base_scale)
                
                def draw_text_with_bg(img, text, position, font_scale, text_color, bg_color, thickness=3):
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
                    x, y = position
                    cv2.rectangle(img, (x, y - text_h - padding), (x + text_w + padding, y + baseline + padding), bg_color, -1)
                    cv2.putText(img, text, (x + int(padding/2), y), font, font_scale, text_color, thickness)
                    return y + baseline + padding

                text_y = draw_text_with_bg(annotated_image, f"Exercise: {state_info['movement_name']}", (margin_x, text_y), font_scale, (255, 255, 255), (0, 0, 0), thickness) + int(20 * base_scale)
                text_y = draw_text_with_bg(annotated_image, f"Target: {state_info['position_name']}", (margin_x, text_y), font_scale, (255, 255, 0), (0, 0, 0), thickness) + int(20 * base_scale)
                text_y = draw_text_with_bg(annotated_image, f"Reps: {state_info['current_reps']} / {state_info['target_reps']}", (margin_x, text_y), font_scale, (0, 255, 255), (0, 0, 0), thickness) + int(40 * base_scale)
                
                # Draw Pose Image
                pose_path = state_info.get("pose_image_path")
                if pose_path:
                    pose_img = self._get_image(pose_path)
                    if pose_img is not None:
                        # Resize pose image to fit in the UI (~23% of width)
                        target_w = int(w * 0.23)
                        aspect_ratio = pose_img.shape[0] / pose_img.shape[1]
                        target_h = int(target_w * aspect_ratio)
                        pose_img_resized = cv2.resize(pose_img, (target_w, target_h))
                        
                        # Place in top right corner
                        margin = int(20 * base_scale)
                        start_x = w - target_w - margin
                        start_y = margin
                        
                        # Draw a border around the pose image
                        border = int(5 * base_scale)
                        cv2.rectangle(annotated_image, (start_x - border, start_y - border), (start_x + target_w + border, start_y + target_h + border), (255, 255, 255), -1)
                        annotated_image[start_y:start_y+target_h, start_x:start_x+target_w] = pose_img_resized

                # Draw a massive hold progress bar
                bar_x = margin_x
                bar_y = text_y
                bar_width = int(w * 0.3)
                bar_height = int(40 * base_scale)
                progress = state_info['hold_progress']
                
                # Background
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)
                # Foreground progress
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + int(bar_width * progress), bar_y + bar_height), (0, 255, 0), -1)
                # Border
                cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), thickness)
                
                # Debug Info at bottom
                debug_info = state_info.get("debug_info", "")
                if debug_info:
                    cv2.putText(annotated_image, f"DEBUG: {debug_info}", (margin_x, h - int(30 * base_scale)), cv2.FONT_HERSHEY_SIMPLEX, 1.2 * base_scale, (255, 255, 255), max(1, int(2 * base_scale)))
                    
                # Scale Factor at bottom
                scale_factor = state_info.get("scale_factor", 1.0)
                cv2.putText(annotated_image, f"SCALE: {scale_factor:.3f}", (margin_x, h - int(80 * base_scale)), cv2.FONT_HERSHEY_SIMPLEX, 1.2 * base_scale, (255, 255, 255), max(1, int(2 * base_scale)))
                
        return annotated_image