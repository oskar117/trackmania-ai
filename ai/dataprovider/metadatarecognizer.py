import re

import cv2
from pytesseract import pytesseract
import numpy as np
from ai.dataprovider.readmemory import MemoryReader


class MetaDataRecognizer:

    def extract_data(self, img=None) -> tuple:
        pass

    def needs_image(self):
        pass


class ImageDataRecognizer(MetaDataRecognizer):

    def __init__(self):
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.custom_config = r'--oem 3 --psm 6'

    def needs_image(self) -> bool:
        return True

    def get_value(self, img: np.array):
        str_value = pytesseract.image_to_string(img, config=self.custom_config)
        return int(re.sub('[^0-9-]', '', str_value.strip().replace('o', '0')))

    def extract_data(self, img=None):
        width, height = img.shape[:2]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img = 255 - img
        speed_img = img[666:666 + 40, 1050:1050 + 130]
        speed = self.get_value(speed_img)
        gear_img = img[666:666 + 40, 950:950 + 130]
        gear = self.get_value(gear_img)
        distance_img = img[666:666 + 40, 1180:1180 + 130]
        distance = self.get_value(distance_img)
        return speed, gear, distance


class MemoryDataRecognizer(MetaDataRecognizer):

    def __init__(self, args: tuple) -> None:
        if len(args) != 6:
            raise AttributeError(f"Wrong number of parameters: '{len(args)}' instead of 6")
        self.memory_reader = MemoryReader(int(args[0], 16))
        self.speed_addr = self.str_to_hex(args[1])
        self.gear_addr = self.str_to_hex(args[2])
        self.checkpoint_number_addr = self.str_to_hex(args[3])
        self.checkpoint_time_addr = self.str_to_hex(args[4])
        self.lap_time_addr = self.str_to_hex(args[5])

    @staticmethod
    def str_to_hex(string: str) -> int:
        hex_int = int(string, 16)
        return hex_int

    def needs_image(self) -> bool:
        return False

    def extract_data(self, img=None) -> tuple:
        speed = self.memory_reader.read(self.speed_addr)
        gear = self.memory_reader.read(self.gear_addr)
        checkpoints_passed = self.memory_reader.read(self.checkpoint_number_addr)
        last_checkpoint_time = self.memory_reader.read(self.checkpoint_time_addr)
        final_time = self.memory_reader.read(self.lap_time_addr)
        return speed, gear, checkpoints_passed, last_checkpoint_time, final_time
