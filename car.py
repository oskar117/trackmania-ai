import pydirectinput


class Car:

    def drive(self, input):
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
