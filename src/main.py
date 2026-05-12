# main.py
from pathlib import Path

MODLES_DIR = Path(__file__).parent / "../models"
MODEL_PATH = MODLES_DIR / "pose_landmarker_lite.task"


def main():
    print(MODEL_PATH)

if __name__ == "__main__":
    main()