import operator

# Normalization modalities
NORM_MODALITY_TORSO = "torso"
NORM_MODALITY_NONE = "none"

# Core condition types
COND_ABS_DIST_X = "abs_distance_x"
COND_ABS_DIST_Y = "abs_distance_y"
COND_ANGLE = "angle"

CONDITION_TYPES = {
    COND_ABS_DIST_X,
    COND_ABS_DIST_Y,
    COND_ANGLE
}

# Custom landmark indices
CG_INDEX = -1

# Landmark mappings
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
    "CG": CG_INDEX 
}

# Operator string to python operator function mappings
OPERATOR_MAP = {
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne
}