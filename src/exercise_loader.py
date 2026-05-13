# exercise_loader.py

import json
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