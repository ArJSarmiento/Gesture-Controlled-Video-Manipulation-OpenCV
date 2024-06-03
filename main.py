"""
    Final Project for Computer Vision
    Arnel Jan Sarmiento
    BSCS - 3
    2021-05094
"""

import math

import cv2
import numpy as np

from hand_tracking import HandDetector

# Camera resolution
w_cam, h_cam = 1280, 720

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)

# Initialize hand detector
detector = HandDetector(detection_con=0.7)

# Angle and length variables
last_angle = None
last_length = None

min_angle = 0
max_angle = 180
min_hand = 50
max_hand = 300
angle_bar = 400
angle_deg = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=False)

    if lm_list:
        # Get the positions of the thumb and index finger
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw circles and line
        cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

        # Calculate the length between the two points
        length = math.hypot(x2 - x1, y2 - y1)

        # Interpolate angle and angle bar values
        angle = np.interp(length, [min_hand, max_hand], [min_angle, max_angle])
        angle_bar = np.interp(length, [min_hand, max_hand], [400, 150])
        angle_deg = np.interp(length, [min_hand, max_hand], [0, 180])

        # Update last length and angle
        last_angle = angle
        last_length = length

        # Draw green circle if length is below threshold
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Draw angle bar and text
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(angle_bar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(angle_deg)} deg', (40, 90), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
