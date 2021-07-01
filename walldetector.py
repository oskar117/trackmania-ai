import math

import cv2
import numpy as np
from sklearn import preprocessing

class WallDetector:

    DILATION_SIZE = 6
    KERNEL_ELLIPSE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * DILATION_SIZE + 1, 2 * DILATION_SIZE + 1), (5, 5))
    KERNEL_SQUARE = np.array((2, 2), np.uint8)

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_distances(self, image):
        image = self.transform_perspective(image)
        mask = self.filter_black_colour(image)
        mask = self.filter_contours(mask)
        test = self.calculate_and_draw(image, mask)
        test = tuple(preprocessing.normalize(np.array(test).reshape(1, -1))[0])
        print(test)
        cv2.putText(image, ''.join("{:10.2f}".format(_) for _ in test), (0, 698), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 0, cv2.LINE_AA)
        cv2.imshow('Computer Vision6', image)
        cv2.waitKey(1)
        return test

    def filter_black_colour(self, image):
        mask = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(mask, (0, 0, 0), (255, 255, 70))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.KERNEL_ELLIPSE)
        return cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.KERNEL_SQUARE)

    def transform_perspective(self, image):
        width, height = image.shape[:2]
        points_source = np.float32([[0, 0], [height, 0], [height, width], [0, width]])
        points_dest = np.float32([[height * 0.33, width * 0.45], [height * 0.66, width * 0.45], [height, width], [0, width]])
        transformed_matrix = cv2.getPerspectiveTransform(points_dest, points_source)
        image = cv2.warpPerspective(image, transformed_matrix, (height, width))
        return cv2.resize(image, (self.width, self.height))

    def filter_contours(self, image):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contour_mask = np.zeros_like(image)
        for contour in contours:
            if cv2.contourArea(contour, False) > 1000:
                cv2.drawContours(contour_mask, [contour], -1, (255, 255, 255), 3)
        return contour_mask

    def calculate_and_draw_line(self, degree, image, mask):
        if 90 > degree >= 0:
            return self.calculate_and_draw_0_to_90(degree, image, mask)
        if 180 >= degree > 90:
            return self.calculate_and_draw_90_to_180(180 - degree, image, mask)
        else:
            return self.calculate_and_draw_90(image, mask)

    def calculate_and_draw_0_to_90(self, degree, image, mask):
        y, current_height = 0, 0
        angle = np.tan(np.deg2rad(degree))
        half_width = int(self.width / 2)
        for y in range(half_width - 1, 0, -1):
            current_height = int(angle * (half_width - 1 - y))
            coord_value = mask[self.height - 1 - current_height][y]
            cv2.line(image, (half_width, self.height), (y, self.height - current_height), (0, 255, 0), 2)
            if np.any(coord_value == (255, 255, 255)):
                break
        return math.hypot(half_width - y - 1, current_height)

    def calculate_and_draw_90_to_180(self, degree, image, mask):
        y, current_height = 0, 0
        angle = np.tan(np.deg2rad(degree))
        half_width = int(self.width / 2)
        for y in range(0, half_width - 1):
            current_height = int(angle * y)
            coord_value = mask[self.height - 1 - current_height][y + half_width]
            cv2.line(image, (half_width, self.height), (y + half_width, self.height - current_height), (0, 255, 0), 2)
            if np.any(coord_value == (255, 255, 255)):
                break
        return math.hypot(y, current_height)

    def calculate_and_draw_90(self, image, mask):
        y = 0
        half_width = int(self.width / 2)
        for y in range(self.height - 1, 0, -1):
            coord_value = mask[y][half_width]
            cv2.line(image, (half_width, self.height), (half_width, y), (0, 255, 0), 2)
            if np.any(coord_value == (255, 255, 255)):
                break
        return math.hypot(0, self.height - y - 1)

    def calculate_and_draw(self, image, mask):
        return [self.calculate_and_draw_line(_, image, mask) for _ in range(1, 180) if _ % 15 == 0]
