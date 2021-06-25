from time import time

from cv2 import cv2

from walldetector import WallDetector
from windowcapture import WindowCapture

wincap = WindowCapture('TrackMania')

loop_time = time()

while True:
    i = wincap.get_screenshot()
    wall_detector = WallDetector(700, 700)
    wall_detector.calculate_distances(i)


    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break

print('Done.')
