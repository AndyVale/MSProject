# Multimodal Interactive System: Sportsman Exercise Tracker

This project is an interactive computer vision system that tracks and evaluates user exercises (specifically leg extensions) using a webcam. It uses **MediaPipe** for pose estimation and a **JSON-based State Machine** to dynamically load and evaluate different exercises.

## Project Structure

The codebase is built on the **Single Responsibility Principle**, splitting data extraction, logic, and visualization into separate modules:

```text
/multimodal_project
│
├── main.py                 # Connects the camera, initializes modules, and runs the main loop.
├── pose_extractor.py       # Handles MediaPipe. Extracts raw landmarks and calculates custom ones (e.g., Center of Gravity).
├── ui_renderer.py          # Handles all OpenCV drawing (skeleton, timers, rep counters).
├── exercise_loader.py      # Parses the JSON file into Python objects.
├── exercise_evaluator.py   # Tracks timers, evaluates landmark constraints, and counts repetitions.
│
├── exercises
│   └── leg_extensions.json # Defines the exercise rules, required positions, hold times, and winning conditions.
├── models
│   └── pose_landmarker_lite.task # MediaPipe model file.
└── utils
    └── utils_camera.py     # Camera initialization helper.
