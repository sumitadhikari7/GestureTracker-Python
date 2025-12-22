# GestureTracker-Python

Real-time hand tracking and landmark detection using **Python**, **OpenCV**, and **MediaPipe**.  
This project detects hands, tracks landmarks, and visualizes them on a live webcam feed with FPS display.

---

## Features

### 1. Hand Tracking

- Real-time hand detection using MediaPipe Hands
- Tracks 21 landmarks per hand
- Supports multiple hands
- Visualizes landmarks and hand connections
- Highlights specific landmarks (e.g., wrist or fingertip)
- Displays FPS on the live feed
- Modular handDetector class for reuse in other projects

### 2. Gesture Experiments

- **Cursor movement**

    - Controlled using index finger position
    - Implemented with smoothing to reduce jitter

- **Scroll control**

    - Downward scroll using index + middle finger movement
    - Implemented using simulated input events

- **Click gesture**

    - Triggered using a three-finger gesture
---

