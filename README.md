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

## Platform Limitations

- Gesture based system control but only works on X11.
- Doesn't work on Wayland due to security restrictions on fake input
- Zoom Gestures:
    - The console detected the input but the action didn't work:
        - On Wayland sessions, simulated input is blocked entirely for security reasons.
        - Even on X11 (Xorg), zoom behavior varies by: Window manager, Application, Focus state
    - Removed from Final Implementation
- Volume Control Gestures:
    - Implemented Experimentally
    - Not stable or consistent, depends on system audio backend
- Due to these limitations, the gesture actions may behave unusually
 --- 
## Known Issues

- Reliable global zoom control
- Stable volume control using pinch gestures
- Touchpad-level smoothness for cursor movement
- Gesture actions on Wayland sessions

 **These issues are primarily caused by:**
 - OS Level input restrictions
 - Latency from real-time hand tracking