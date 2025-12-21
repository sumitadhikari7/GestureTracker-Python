import cv2
import time
from Xlib import X, display
from Xlib.ext import xtest
from handtracking import handDetector

SCROLL_THRESHOLD = 5   # Minimum downward movement to trigger scroll
SCROLL_AMOUNT = 3      # Scroll steps per gesture

d = display.Display()

def scroll_down():
    for _ in range(SCROLL_AMOUNT):
        xtest.fake_input(d, X.ButtonPress, 5)   # scroll down
        xtest.fake_input(d, X.ButtonRelease, 5)
    d.sync()

def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    prevY = None
    pTime = 0

    print("Gesture scrolling active: scroll only when finger moves DOWN.")

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            y = lmList[8][2]  # index finger tip Y

            if prevY is not None:
                diff = y - prevY  # positive if finger moved down
                if diff > SCROLL_THRESHOLD:
                    scroll_down()

            prevY = y
        else:
            prevY = None  # reset when hand disappears

        # Show FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Gesture Scroll", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
