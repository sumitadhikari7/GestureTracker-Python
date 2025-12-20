# GestureTracker-Python

Real-time hand tracking and landmark detection using **Python**, **OpenCV**, and **MediaPipe**.  
This project detects hands, tracks landmarks, and visualizes them on a live webcam feed with FPS display.

---

## Features

- Detects **one or multiple hands** in real-time.
- Tracks **21 hand landmarks** per hand.
- Highlights the **wrist landmark (id 0)** with a circle.
- Prints coordinates of specific landmarks (example: tip of the index finger, id 4).
- Displays **frames per second (FPS)** on the video feed.
- Modular code with `handDetector` class for easy integration into other projects.
