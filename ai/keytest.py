import time

import pydirectinput

while True:
    time.sleep(5)
    pydirectinput.keyDown('up')
    pydirectinput.keyDown('right')
    time.sleep(5)
    pydirectinput.keyUp('up')
    pydirectinput.keyUp('right')
