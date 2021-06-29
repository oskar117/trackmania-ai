import re

import cv2
from pytesseract import pytesseract


class MetaDataRecognizer:

    def __init__(self):
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.custom_config = r'--oem 3 --psm 6'

    def get_value(self, img):
        w, h = img.shape[:2]
        str_value = pytesseract.image_to_string(img, config=self.custom_config)
        return int(re.sub('[^0-9-]', '', str_value.strip().replace('o', '0')))

    def extract_data(self, img):
        width, height = img.shape[:2]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img = 255 - img
        speed_img = img[666:666+40, 1050:1050+130]
        speed = self.get_value(speed_img)
        gear_img = img[666:666+40, 950:950+130]
        gear = self.get_value(gear_img)
        distance_img = img[666:666+40, 1180:1180+130]
        distance = self.get_value(distance_img)
        return gear, speed, distance
