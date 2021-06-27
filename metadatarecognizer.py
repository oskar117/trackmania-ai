import re

import cv2
from pytesseract import pytesseract


class MetaDataRecognizer:

    def get_value(self, img):
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        img = 255 - img
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        custom_config = r'--oem 3 --psm 6'
        return int(re.sub('\\D', '', pytesseract.image_to_string(img, config=custom_config)))

    def extract_data(self, img):
        width, height = img.shape[:2]
        speed_img = img[666:666+40, 1050:1050+130]
        speed = self.get_value(speed_img)
        gear_img = img[666:666+40, 950:950+130]
        gear = self.get_value(gear_img)
        distance_img = img[666:666+40, 1180:1180+130]
        distance = self.get_value(distance_img)
        return gear, speed, distance
