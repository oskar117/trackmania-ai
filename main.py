import os
import time

import pytesseract as pytesseract
import pywintypes

import pywintypes
import win32file
import win32pipe
from cv2 import cv2

import readmemory
from metadatarecognizer import MetaDataRecognizer
from walldetector import WallDetector
from windowcapture import WindowCapture

wincap = WindowCapture('TrackMania')

# loop_time = time()

while True:
    i = wincap.get_screenshot()
    wall_detector = WallDetector(700, 700)
    distances = wall_detector.calculate_distances(i)

    # print('lap time: ',  readmemory.GetSpeed(0x00001CD8, 0x7FF6E95DCA04))
    # print('last checkpoint: ',  readmemory.GetSpeed(0x00001CD8, 0x26EBC5B0C98))
    # print('final_lap_time: ',  readmemory.GetSpeed(0x00001CD8, 0x26F57D40E78))
    # print('speed: ', readmemory.GetSpeed(0x00002854, 0x26F57826F98))

    mdr = MetaDataRecognizer()
    mdr.extract_data(i)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break

print('Done.')
