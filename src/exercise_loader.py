# exercise_loader.py

import json
import os
from utils.constants import LANDMARK_MAP, OPERATOR_MAP, CONDITION_TYPES

# ==========================================
# DATA STRUCTURES
# ==========================================

class Constraint:
    def __init__(self, constraint_type: str, landmarks: list, op_str: str, value: float):
        if constraint_type not in CONDITION_TYPES:
            raise ValueError(f"Unsupported constraint type: {constraint_type}")
        
        self.type = constraint_type
        # Convert string landmark names to mapped integers
        self.landmarks = [LANDMARK_MAP[lm] for lm in landmarks]
        self.operator = OPERATOR_MAP[op_str]
        self.value = value

    def __repr__(self):
        return f"Constraint(type='{self.type}', landmarks={self.landmarks}, operator={self.operator.__name__}, value={self.value})"


class Position:
    def __init__(self, name: str, hold_time_seconds: float, constraints: list, pose_image_path: str = None):
        self.name = name
        self.hold_time_seconds = hold_time_seconds
        self.constraints = constraints
        # Absolute path to the pose image for this position, or None if not provided
        self.pose_image_path = pose_image_path

    def __repr__(self):
        return f"Position(name='{self.name}', hold_time={self.hold_time_seconds}s, constraints={len(self.constraints)})"


class Movement:
    def __init__(self, movement_id: str, name: str, normalization_modality: str, required_landmarks: list, sequence: list):
        self.id = movement_id
        self.name = name
        self.normalization_modality = normalization_modality
        # Convert to mapped integers
        self.required_landmarks = [LANDMARK_MAP[lm] for lm in required_landmarks]
        self.sequence = sequence

    def __repr__(self):
        return f"Movement(id='{self.id}', name='{self.name}', norm='{self.normalization_modality}', positions={len(self.sequence)})"


# ==========================================
# EXERCISE LOADER
# ========================================== 

class ExerciseLoader:
    def __init__(self, exercise_plan_path: str):
        self.movements = {}
        self.training = []
        
        if exercise_plan_path:
            self.load_exercise_plan(exercise_plan_path)

    def load_exercise_plan(self, exercise_plan_path: str):
        """
        Loads the exercise from a JSON file inside an exercise folder and
        populates the various attributes.

        The exercise_plan_path should point to the JSON file inside the exercise
        folder (e.g. 'exercises/leg_ext/leg_ext.json'). Pose images referenced
        in the JSON via the 'pose_image' field are resolved relative to the
        directory that contains the JSON file.
        """
        # Resolve the base directory of the JSON so we can build absolute paths
        # for pose images stored in the sibling 'poses/' folder.
        exercise_dir = os.path.dirname(os.path.abspath(exercise_plan_path))

        with open(exercise_plan_path, 'r') as f:
            data = json.load(f)
            
        # Parse Movements
        movements_data = data.get("movements", {})
        for movement_id, m_data in movements_data.items():
            
            sequence_list = []
            for pos_data in m_data.get("sequence", []):
                
                constraints_list = []
                for c_data in pos_data.get("constraints", []):
                    constraint = Constraint(
                        constraint_type=c_data["type"],
                        landmarks=c_data["landmarks"],
                        op_str=c_data["operator"],
                        value=c_data["value"]
                    )
                    constraints_list.append(constraint)

                # Resolve the pose image path relative to the exercise directory
                pose_image_rel = pos_data.get("pose_image", None)
                pose_image_abs = None
                if pose_image_rel:
                    candidate = os.path.join(exercise_dir, pose_image_rel)
                    if os.path.isfile(candidate):
                        pose_image_abs = candidate

                position = Position(
                    name=pos_data["position_name"],
                    hold_time_seconds=pos_data.get("hold_time_seconds", 0.0),
                    constraints=constraints_list,
                    pose_image_path=pose_image_abs
                )
                sequence_list.append(position)
                
            movement = Movement(
                movement_id=movement_id,
                name=m_data.get("name", ""),
                normalization_modality=m_data.get("normalization_modality", "none"),
                required_landmarks=m_data.get("required_landmarks", []),
                sequence=sequence_list
            )
            self.movements[movement_id] = movement
            
        # Parse Training (keep as a list of dicts for now)
        self.training = data.get("training", [])