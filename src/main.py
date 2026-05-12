# main.py
import cv2
import time
import mediapipe as mp
from pathlib import Path

MODLES_DIR = Path(__file__).parent / "../models"
MODEL_PATH = MODLES_DIR / "pose_landmarker_lite.task"

from utils.utils_camera import init_camera

# Import our new modular components
from pose_extractor import PoseExtractor
from ui_renderer import UIRenderer
from exercise_loader import ExerciseLoader

def main():
    camera_capture = init_camera(width=2048 , height=1536, index=0)
    
    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode
    
    loader = ExerciseLoader("exercises/leg_ext.json")
    
    # Collect all required landmarks across all movements
    required_landmarks = set()
    for movement in loader.movements.values():
        required_landmarks.update(movement.required_landmarks)
        
    # Components used to extract the landmarks and draw the UI
    extractor = PoseExtractor(list(required_landmarks))
    renderer = UIRenderer()
    
    from exercise_evaluator import ExerciseEvaluator
    evaluator = ExerciseEvaluator(loader.movements, loader.training)
    

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=extractor.process_result)

    initial_time = time.time()
    
    with PoseLandmarker.create_from_options(options) as landmarker:
        while True:
            success, current_frame = camera_capture.read()
            if not success:
                break
                
            current_frame = cv2.flip(current_frame, 1)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=current_frame)
            
            frame_timestamp_ms = int((time.time() - initial_time) * 1000)
            landmarker.detect_async(mp_image, frame_timestamp_ms)
            
            current_image = extractor.latest_image
            current_result = extractor.latest_result
            
            if current_result is not None and current_image is not None:
                current_time = time.time()
                evaluator.update(current_result, current_time)
                state_info = evaluator.get_state(current_time)
                
                annotated_image = renderer.draw(current_image, current_result, state_info)
                cv2.imshow("Mediapipe Pose Landmarker", annotated_image)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    camera_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()