# exercise_loader.py

import json
import operator

# ==========================================
# CONSTANT MAPPINGS
# ==========================================

LANDMARK_MAP = {
    # Head and Face
    "NOSE": 0, "LEFT_EYE_INNER": 1, "LEFT_EYE": 2, "LEFT_EYE_OUTER": 3,
    "RIGHT_EYE_INNER": 4, "RIGHT_EYE": 5, "RIGHT_EYE_OUTER": 6,
    "LEFT_EAR": 7, "RIGHT_EAR": 8, "MOUTH_LEFT": 9, "MOUTH_RIGHT": 10,
    # Torso and Arms
    "LEFT_SHOULDER": 11, "RIGHT_SHOULDER": 12,
    "LEFT_ELBOW": 13, "RIGHT_ELBOW": 14,
    "LEFT_WRIST": 15, "RIGHT_WRIST": 16,
    "LEFT_PINKY": 17, "RIGHT_PINKY": 18,
    "LEFT_INDEX": 19, "RIGHT_INDEX": 20,
    "LEFT_THUMB": 21, "RIGHT_THUMB": 22,
    "LEFT_HIP": 23, "RIGHT_HIP": 24,
    # Legs
    "LEFT_KNEE": 25, "RIGHT_KNEE": 26,
    "LEFT_ANKLE": 27, "RIGHT_ANKLE": 28,
    "LEFT_HEEL": 29, "RIGHT_HEEL": 30,
    "LEFT_FOOT_INDEX": 31, "RIGHT_FOOT_INDEX": 32,
    # Custom Calculations
    "CG": -1 
}

OPERATOR_MAP = {
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne
}

CONDITION_TYPES = {
    "abs_distance_x",
    "abs_distance_y",
    "angle"
}

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
    def __init__(self, name: str, hold_time_seconds: float, constraints: list):
        self.name = name
        self.hold_time_seconds = hold_time_seconds
        self.constraints = constraints

    def __repr__(self):
        return f"Position(name='{self.name}', hold_time={self.hold_time_seconds}s, constraints={len(self.constraints)})"


class Movement:
    def __init__(self, movement_id: str, name: str, required_landmarks: list, sequence: list):
        self.id = movement_id
        self.name = name
        # Convert to mapped integers
        self.required_landmarks = [LANDMARK_MAP[lm] for lm in required_landmarks]
        self.sequence = sequence

    def __repr__(self):
        return f"Movement(id='{self.id}', name='{self.name}', positions={len(self.sequence)})"


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
        Loads the exercise from a JSON file and populates the various attributes.
        """
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
                    
                position = Position(
                    name=pos_data["position_name"],
                    hold_time_seconds=pos_data.get("hold_time_seconds", 0.0),
                    constraints=constraints_list
                )
                sequence_list.append(position)
                
            movement = Movement(
                movement_id=movement_id,
                name=m_data.get("name", ""),
                required_landmarks=m_data.get("required_landmarks", []),
                sequence=sequence_list
            )
            self.movements[movement_id] = movement
            
        # Parse Training (keep as a list of dicts for now)
        self.training = data.get("training", [])