import cv2
import time
import pyautogui
from handtracking import handDetector
import math
import os

pyautogui.FAILSAFE = False

# ---------------------------
# Helper functions
# ---------------------------
def fingers_up(lmList, threshold=30):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if lmList[tips[0]][1] > lmList[tips[0]-1][1] + threshold:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for id in range(1,5):
        if lmList[tips[id]][2] < lmList[tips[id]-2][2] - threshold:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

# ---------------------------
# Main program
# ---------------------------
def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    prevY_scroll = None
    prevX, prevY = 0, 0
    emaX, emaY = 0, 0  # for exponential smoothing

    screenWidth, screenHeight = pyautogui.size()
    frameWidth, frameHeight = 640, 480
    alpha = 0.5  # smoothing factor (0=very smooth, 1=no smoothing)

    last_volume = -1  # track last volume to reduce frequent updates

    print("Gesture control started. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            continue

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            fingers = fingers_up(lmList)

            # ---------- Cursor move (index finger only) ----------
            if sum(fingers) == 1 and fingers[1] == 1:
                x = lmList[8][1]
                y = lmList[8][2]

                # Map to screen (invert X)
                screenX = screenWidth - (screenWidth * x / frameWidth)
                screenY = screenHeight * y / frameHeight

                # Exponential smoothing
                emaX = alpha * screenX + (1 - alpha) * emaX
                emaY = alpha * screenY + (1 - alpha) * emaY

                pyautogui.moveTo(int(emaX), int(emaY), duration=0)
                prevY_scroll = None

            # ---------- Scroll down (index + middle fingers) ----------
            elif sum(fingers) == 2 and fingers[1] == 1 and fingers[2] == 1:
                y_mid = (lmList[8][2] + lmList[12][2]) // 2
                if prevY_scroll is not None:
                    diff = y_mid - prevY_scroll
                    if diff > 3:  # scroll only downward
                        pyautogui.scroll(-40)
                prevY_scroll = y_mid

            # ---------- Click (3 fingers) ----------
            elif sum(fingers) == 3:
                pyautogui.click()
                time.sleep(0.5)
                prevY_scroll = None

            # ---------- Volume control (thumb + index) ----------
            elif fingers[0] == 1 and fingers[1] == 1:
                thumb_tip = (lmList[4][1], lmList[4][2])
                index_tip = (lmList[8][1], lmList[8][2])
                dist = distance(thumb_tip, index_tip)

                # Map distance to 0-100% volume
                vol = int(min(max((dist - 30) * 100 / 170, 0), 100))

                # Update volume only if changed significantly
                if abs(vol - last_volume) >= 2:
                    os.system(f"amixer -D pulse sset Master {vol}% > /dev/null")
                    last_volume = vol

                prevY_scroll = None

            else:
                prevY_scroll = None

        else:
            prevY_scroll = None

        cv2.imshow("Gesture Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
