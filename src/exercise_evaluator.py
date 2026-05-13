# exercise_evaluator.py
import numpy as np
from utils.constants import COND_ABS_DIST_X, COND_ABS_DIST_Y, COND_DIST_X, COND_DIST_Y, COND_ANGLE

class ExerciseEvaluator:
    def __init__(self, movements: dict, training: list):
        self.movements = movements
        self.training = training
        
        self.current_training_index = 0
        self.current_reps = 0
        self.current_position_index = 0
        self.hold_start_time = None
        self.last_debug_info = ""

    def get_current_modality(self) -> str:
        """Returns the normalization modality of the current movement."""
        if self.current_training_index >= len(self.training):
            return "none"
        training_item = self.training[self.current_training_index]
        movement = self.movements[training_item["movement"]]
        return movement.normalization_modality

    def _calculate_distance(self, l1, l2, scale_factor: float, axis=None, signed=False):
        """
        Calculates distance between two landmarks using numpy, then normalizes by the scale_factor.
        """
        p1 = np.array([l1['x'], l1['y'], l1['z']])
        p2 = np.array([l2['x'], l2['y'], l2['z']])
        
        if axis == 'x':
            dist = (p1[0] - p2[0]) / scale_factor
            return dist if signed else abs(dist)
        elif axis == 'y':
            dist = (p1[1] - p2[1]) / scale_factor
            return dist if signed else abs(dist)
        else:
            return np.linalg.norm(p1 - p2) / scale_factor

    def _evaluate_constraint(self, constraint, landmarks_dict, scale_factor) -> bool:
        """
        Evaluates a single constraint and stores debug info.
        """
        # Ensure the required landmarks are present
        for lm in constraint.landmarks:
            if lm not in landmarks_dict:
                self.debug_info = f"Missing landmark idx: {lm}"
                return False

        if constraint.type == COND_ABS_DIST_X:
            l1, l2 = landmarks_dict[constraint.landmarks[0]], landmarks_dict[constraint.landmarks[1]]
            norm_val = self._calculate_distance(l1, l2, scale_factor, axis='x')
            raw_val = norm_val * scale_factor
            result = constraint.operator(norm_val, constraint.value)
            self.debug_info = f"norm_dx={norm_val:.3f} (raw={raw_val:.3f}, target={constraint.value}) -> {result}"
            return result
            
        elif constraint.type == COND_ABS_DIST_Y:
            l1, l2 = landmarks_dict[constraint.landmarks[0]], landmarks_dict[constraint.landmarks[1]]
            norm_val = self._calculate_distance(l1, l2, scale_factor, axis='y')
            raw_val = norm_val * scale_factor
            result = constraint.operator(norm_val, constraint.value)
            self.debug_info = f"norm_dy={norm_val:.3f} (raw={raw_val:.3f}, target={constraint.value}) -> {result}"
            return result
            
        elif constraint.type == COND_DIST_X:
            l1, l2 = landmarks_dict[constraint.landmarks[0]], landmarks_dict[constraint.landmarks[1]]
            norm_val = self._calculate_distance(l1, l2, scale_factor, axis='x', signed=True)
            result = constraint.operator(norm_val, constraint.value)
            self.debug_info = f"norm_dist_x={norm_val:.3f} (target={constraint.value}) -> {result}"
            return result

        elif constraint.type == COND_DIST_Y:
            l1, l2 = landmarks_dict[constraint.landmarks[0]], landmarks_dict[constraint.landmarks[1]]
            norm_val = self._calculate_distance(l1, l2, scale_factor, axis='y', signed=True)
            result = constraint.operator(norm_val, constraint.value)
            self.debug_info = f"norm_dist_y={norm_val:.3f} (target={constraint.value}) -> {result}"
            return result
            
        elif constraint.type == COND_ANGLE:
            self.debug_info = "Angle constraint not implemented"
            return False 

        self.debug_info = f"Unknown constraint: {constraint.type}"
        return False

    def update(self, landmarks_dict: dict, scale_factor: float, current_time: float):
        if self.current_training_index >= len(self.training):
            return # Training complete
            
        training_item = self.training[self.current_training_index]
        movement = self.movements[training_item["movement"]]
        position = movement.sequence[self.current_position_index]
        
        # Check all constraints
        all_met = True
        debug_strings = []
        for constraint in position.constraints:
            met = self._evaluate_constraint(constraint, landmarks_dict, scale_factor)
            debug_strings.append(self.debug_info)
            if not met:
                all_met = False
                # Do not break here so we can see all debug strings in the UI
                
        self.last_debug_info = " | ".join(debug_strings)
                
        if all_met:
            if self.hold_start_time is None:
                self.hold_start_time = current_time
                
            if current_time - self.hold_start_time >= position.hold_time_seconds:
                # Transition to next position
                self.current_position_index += 1
                self.hold_start_time = None
                
                # Check if movement sequence is complete
                if self.current_position_index >= len(movement.sequence):
                    self.current_reps += 1
                    self.current_position_index = 0
                    
                    # Check if reps are complete
                    if self.current_reps >= training_item["repetitions"]:
                        self.current_training_index += 1
                        self.current_reps = 0
        else:
            # Violated constraint, user must hold pose continuously
            self.hold_start_time = None

    def get_state(self, current_time: float) -> dict:
        if self.current_training_index >= len(self.training):
            return {
                "is_completed": True,
                "movement_name": "",
                "position_name": "",
                "current_reps": 0,
                "target_reps": 0,
                "hold_progress": 0.0,
                "debug_info": ""
            }
            
        training_item = self.training[self.current_training_index]
        movement = self.movements[training_item["movement"]]
        position = movement.sequence[self.current_position_index]
        
        hold_progress = 0.0
        if self.hold_start_time is not None and position.hold_time_seconds > 0:
            hold_progress = min(1.0, (current_time - self.hold_start_time) / position.hold_time_seconds)
            
        return {
            "is_completed": False,
            "movement_name": movement.name,
            "position_name": position.name,
            "current_reps": self.current_reps,
            "target_reps": training_item["repetitions"],
            "hold_progress": hold_progress,
            "debug_info": getattr(self, "last_debug_info", "")
        }
