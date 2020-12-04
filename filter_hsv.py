import numpy as np
import cv2


class Webcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.Lower_blue = np.array([110, 120, 120])
        self.Upper_blue = np.array([130, 255, 255])

    def update_frame(self):
        img = self.cap.read()[1]
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        kernel = np.ones((5, 5), np.uint8)
        mask1 = cv2.inRange(hsv, self.Lower_blue, self.Upper_blue)
        mask2 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)
        # mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)
        # mask2 = cv2.morphologyEx(mask2, cv2.MORPH_GRADIENT, kernel)
        mask = cv2.dilate(mask2, kernel, iterations=1)
        contour, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)[-2:]

        if len(contour) > 0:
            c = min(contour, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            return x, y
