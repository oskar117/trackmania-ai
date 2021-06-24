import math
import sys
from time import time

import numpy as np
from cv2 import cv2

from windowcapture import WindowCapture

wincap = WindowCapture('TrackMania')

loop_time = time()

lowH = 0
lowS = 0
lowV = 0

highH = 255
highS = 255
highV = 70

while True:
    i = wincap.get_screenshot()
    screenshot = i

    dilation_size = 6
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * dilation_size + 1, 2 * dilation_size + 1), (5, 5))

    width, height, channels = i.shape
    # perspective
    pts1 = np.float32([[height * 0.33, width * 0.45], [height * 0.66, width * 0.45], [height, width], [0, width]])
    pts2 = np.float32([[0, 0], [height, 0], [height, width], [0, width]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    i = cv2.warpPerspective(i, M, (height, width))
    i = cv2.resize(i, (700, 700))

    mask = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(mask, (lowH, lowS, lowV), (highH, highS, highV))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.array((2,2), np.uint8))
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    better_mask = np.zeros_like(mask)
    fixed_contours = []
    for contour in contours:
        if cv2.contourArea(contour, False) > 1000:
            # cv2.drawContours(i, [contour], -1, (255, 255, 255), 3)
            fixed_contours.append(contour)
            cv2.drawContours(better_mask, [contour], -1, (255, 255, 255), 3)

    for y in range(350, 0, -1):
        current_height = int(np.tan(45 * np.pi / 180) * (350 - y))
        coord_value = better_mask[699 - current_height][y]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)
            break

    for y in range(350, 0, -1):
        current_height = int(np.tan(30 * np.pi / 180) * (350 - y))
        coord_value = better_mask[699 - current_height][y]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)

    for y in range(350, 0, -1):
        current_height = int(np.tan(15 * np.pi / 180) * (350 - y))
        coord_value = better_mask[699 - current_height][y]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)

    for y in range(350, 0, -1):
        current_height = int(np.tan(75 * np.pi / 180) * (350 - y))
        coord_value = better_mask[699 - current_height][y]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)

    for y in range(350, 0, -1):
        current_height = int(np.tan(60 * np.pi / 180) * (350 - y))
        coord_value = better_mask[699 - current_height][y]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y, 699 - current_height), (0, 255, 0), 2)

    for y in range(0, 350):
        current_height = int(np.tan(15 * np.pi / 180) * y)
        coord_value = better_mask[699 - current_height][y + 350]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)

    for y in range(0, 350):
        current_height = int(np.tan(30 * np.pi / 180) * y)
        coord_value = better_mask[699 - current_height][y + 350]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)

    for y in range(0, 350):
        current_height = int(np.tan(45 * np.pi / 180) * y)
        coord_value = better_mask[699 - current_height][y + 350]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)

    for y in range(0, 350):
        current_height = int(np.tan(60 * np.pi / 180) * y)
        coord_value = better_mask[699 - current_height][y + 350]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)

    for y in range(0, 350):
        current_height = int(np.tan(75 * np.pi / 180) * y)
        coord_value = better_mask[699 - current_height][y + 350]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (y + 350, 699 - current_height), (0, 255, 0), 2)

    for y in range(699, 0, -1):
        coord_value = better_mask[y][350]
        if np.any(coord_value == (255, 255, 255)):
            cv2.line(i, (350, 700), (350, y), (0, 255, 0), 2)
            break
        cv2.line(i, (350, 700), (350, y), (0, 255, 0), 2)

    # cv2.imshow('Computer Vision4', mask)
    # cv2.imshow('Computer Vision5', better_mask)
    cv2.imshow('Computer Vision6', i)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break

print('Done.')
