import operator

# Normalization modalities
NORM_MODALITY_TORSO = "torso"
NORM_MODALITY_NONE = "none"

# Core condition types
COND_ABS_DIST_X = "abs_distance_x"
COND_ABS_DIST_Y = "abs_distance_y"
COND_DIST_X = "distance_x"
COND_DIST_Y = "distance_y"
COND_ANGLE = "angle"

CONDITION_TYPES = {
    COND_ABS_DIST_X,
    COND_ABS_DIST_Y,
    COND_DIST_X,
    COND_DIST_Y,
    COND_ANGLE
}

# Custom landmark indices
CG_INDEX = -1

# Landmark mappings
LANDMARK_MAP = {
    # Head and Face
    "NOSE": 0, "RIGHT_EYE_INNER": 1, "RIGHT_EYE": 2, "RIGHT_EYE_OUTER": 3,
    "LEFT_EYE_INNER": 4, "LEFT_EYE": 5, "LEFT_EYE_OUTER": 6,
    "RIGHT_EAR": 7, "LEFT_EAR": 8, "MOUTH_RIGHT": 9, "MOUTH_LEFT": 10,
    # Torso and Arms
    "RIGHT_SHOULDER": 11, "LEFT_SHOULDER": 12,
    "RIGHT_ELBOW": 13, "LEFT_ELBOW": 14,
    "RIGHT_WRIST": 15, "LEFT_WRIST": 16,
    "RIGHT_PINKY": 17, "LEFT_PINKY": 18,
    "RIGHT_INDEX": 19, "LEFT_INDEX": 20,
    "RIGHT_THUMB": 21, "LEFT_THUMB": 22,
    "RIGHT_HIP": 23, "LEFT_HIP": 24,
    # Legs
    "RIGHT_KNEE": 25, "LEFT_KNEE": 26,
    "RIGHT_ANKLE": 27, "LEFT_ANKLE": 28,
    "RIGHT_HEEL": 29, "LEFT_HEEL": 30,
    "RIGHT_FOOT_INDEX": 31, "LEFT_FOOT_INDEX": 32,
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