import pydirectinput


class Car:

    def __init__(self, wincap, wall_detector, metadata_recognizer) -> None:
        self.__wincap = wincap
        self.__wall_detector = wall_detector
        self.__metadata_recognizer = metadata_recognizer

    def drive(self, net):
        i = self.__wincap.get_screenshot()
        distances = self.__wall_detector.calculate_distances(i)
        if not self.__metadata_recognizer.needs_image:
            i = None
        metadata = self.__metadata_recognizer.extract_data(img=i)
        output = net.activate(distances + metadata)
        self.__steer(output)
        return metadata

    def __steer(self, input):
        up = input[0]
        down = input[1]
        left = input[2]
        right = input[3]

        if up > 0:
            pydirectinput.keyDown('up')
        else:
            pydirectinput.keyUp('up')

        if down > 0:
            pydirectinput.keyDown('down')
        else:
            pydirectinput.keyUp('down')

        if left > 0:
            pydirectinput.keyDown('left')
        else:
            pydirectinput.keyUp('left')

        if right > 0:
            pydirectinput.keyDown('right')
        else:
            pydirectinput.keyUp('right')
