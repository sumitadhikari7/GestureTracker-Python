import cv2
import time
import pyautogui
from handtracking import handDetector
import math
import os

pyautogui.FAILSAFE = False

def fingers_up(lmList, threshold=30):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    fingers.append(1 if lmList[4][1] > lmList[3][1] + threshold else 0)

    for i in range(1, 5):
        fingers.append(1 if lmList[tips[i]][2] < lmList[tips[i]-2][2] - threshold else 0)

    return fingers

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    screenWidth, screenHeight = pyautogui.size()
    frameWidth, frameHeight = 640, 480

    emaX, emaY = 0, 0
    alpha = 0.5
    current_mode = "Idle"
    prev_time = 0

    while True:
        success, img = cap.read()
        if not success:
            continue

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if lmList:
            fingers = fingers_up(lmList)

            if sum(fingers) == 1 and fingers[1] == 1:
                current_mode = "Cursor Move"
                x, y = lmList[8][1], lmList[8][2]
                screenX = screenWidth - (screenWidth * x / frameWidth)
                screenY = screenHeight * y / frameHeight
                emaX = alpha * screenX + (1 - alpha) * emaX
                emaY = alpha * screenY + (1 - alpha) * emaY
                pyautogui.moveTo(int(emaX), int(emaY), duration=0)
            else:
                current_mode = "Idle"

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time

        cv2.putText(img, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f"Mode: {current_mode}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        cv2.imshow("Gesture Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
