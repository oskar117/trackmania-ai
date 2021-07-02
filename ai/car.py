import threading

import pydirectinput
import neat


class Car:

    def __init__(self, window_capture, wall_detector, metadata_recognizer) -> None:
        self.__window_capture = window_capture
        self.__wall_detector = wall_detector
        self.__metadata_recognizer = metadata_recognizer

    def drive(self, net: neat.nn.FeedForwardNetwork) -> (tuple, tuple):
        i = self.__window_capture.get_screenshot()
        distances = self.__wall_detector.calculate_distances(i)
        if not self.__metadata_recognizer.needs_image:
            i = None
        metadata = self.__metadata_recognizer.extract_data(img=i)
        output = net.activate(distances + metadata[:2])
        threading.Thread(target=self.__steer, args=(output,)).start()
        return metadata, distances

    def __steer(self, driver_input: tuple) -> None:

        up = driver_input[0]
        left = driver_input[1]
        right = driver_input[2]

        if up > 0:
            pydirectinput.keyDown('up')
        else:
            pydirectinput.keyUp('up')

        if left > 0:
            pydirectinput.keyDown('left')
        else:
            pydirectinput.keyUp('left')

        if right > 0:
            pydirectinput.keyDown('right')
        else:
            pydirectinput.keyUp('right')
