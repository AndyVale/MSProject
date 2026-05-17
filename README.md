# Multimodal Interactive System: Sportsman Exercise Tracker

This project is an interactive computer vision system that tracks and evaluates user exercises (e.g., bilateral arm raises, leg extensions) using a webcam. It uses **MediaPipe** for pose estimation and a dynamic **JSON-based State Machine** to evaluate landmark constraints, count repetitions, and display visual feedback in real-time.

---

## Project Structure

The codebase is built on the **Single Responsibility Principle**, separating data extraction, business/evaluation logic, visualization, and configuration parsing:

```text
MSProject/
│
├── exercises/                  # Exercise configuration folders
│   ├── arm_raise/
│   │   ├── arm_raise.json      # Configuration defining landmarks and constraints
│   │   └── poses/              # Reference images for position visualizations
│   ├── bilateral_arm_raise/
│   │   ├── bilateral_arm_raise.json
│   │   └── poses/
│   ├── leg_ext/
│   │   ├── leg_ext.json
│   │   └── poses/
│   └── template.json           # Template file for creating new exercises
│
├── models/
│   └── pose_landmarker_lite.task # MediaPipe pre-trained model file
│
├── src/                        # Core Python application source code
│   ├── main.py                 # Application entrypoint & orchestrator loop
│   ├── pose_extractor.py       # Handles MediaPipe pose estimation & custom landmark calculations
│   ├── ui_renderer.py          # Handles all OpenCV screen overlays, progress bars, and guide images
│   ├── exercise_loader.py      # Parses JSON configurations into Object models (Movement, Position, Constraint)
│   ├── exercise_evaluator.py   # State machine tracking movement phases, constraints, and repetitions
│   │
│   └── utils/                  # Helper utilities and shared variables
│       ├── constants.py        # Mappings for landmarks, operators, and screen resolutions
│       └── utils_camera.py     # Webcam stream initialization helper
│
├── requirements.txt            # Python dependencies (numpy, mediapipe, opencv-python)
└── README.md                   # Project documentation
```

---

## Setup Instructions

### 💻 Windows Setup

1. **Clone the Repository:**
   Open PowerShell or Command Prompt (CMD) and run:
   ```cmd
   git clone https://github.com/AndyVale/MSProject.git
   cd MSProject
   ```

2. **Create a Virtual Environment:**
   ```cmd
   python -m venv .venv
   ```

3. **Activate the Virtual Environment:**
   *   **PowerShell:**
       ```powershell
       .\.venv\Scripts\Activate.ps1
       ```
       *(Note: If you run into an execution policy error, execute `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first).*
   *   **Command Prompt (CMD):**
       ```cmd
       .\.venv\Scripts\activate.bat
       ```

4. **Install Dependencies:**
   ```cmd
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Run the Application:**
   ```cmd
   python src/main.py
   ```

---

### 🐧 Linux Setup

1. **Clone the Repository:**
   Open a terminal and run:
   ```bash
   git clone https://github.com/AndyVale/MSProject.git
   cd MSProject
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the Virtual Environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Run the Application:**
   ```bash
   python src/main.py
   ```

---

*Press **`q`** at any time to exit the webcam screen.*