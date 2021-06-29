import multiprocessing
import os
import time

import pydirectinput
import pytesseract as pytesseract
import pywintypes

import pywintypes
import win32file
import win32pipe
from cv2 import cv2
import neat

import readmemory
from metadatarecognizer import MetaDataRecognizer
from walldetector import WallDetector
from windowcapture import WindowCapture

wincap = WindowCapture('TrackMania')
mdr = MetaDataRecognizer()

wall_detector = WallDetector(700, 700)


# loop_time = time()
# print('lap time: ',  readmemory.GetSpeed(0x00001CD8, 0x7FF6E95DCA04))
# print('last checkpoint: ',  readmemory.GetSpeed(0x00001CD8, 0x26EBC5B0C98))
# print('final_lap_time: ',  readmemory.GetSpeed(0x00001CD8, 0x26F57D40E78))
# print('speed: ', readmemory.GetSpeed(0x00002854, 0x26F57826F98))

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


def run_learning(genomes, config):
    cars = []
    nets = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car())

    for index, car in enumerate(cars):

        gen_time = time.time()
        distance_travelled = 0,
        pydirectinput.press('delete')
        while time.time() - gen_time < 20:
            distance_travelled, speed = process_car(nets[cars.index(car)], car)
            if speed < -20:
                break
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
        genomes[index][1].fitness = distance_travelled


def process_car(net, car):
    i = wincap.get_screenshot()
    distances = wall_detector.calculate_distances(i)
    gear, speed, distance = mdr.extract_data(i)
    output = net.activate(distances + (gear, speed, distance))
    car.drive(output)
    return distance, speed


config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                            neat.DefaultStagnation, 'config-feedforward.txt')

p = neat.Population(config)

p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)
time.sleep(5)
p.run(run_learning, 50)
# while True:
#     i = wincap.get_screenshot()
#     distances = wall_detector.calculate_distances(i)
#
#     gear, speed, distance = mdr.extract_data(i)
#     print(gear, speed, distance)
#     if cv2.waitKey(1) == ord('q'):
#         cv2.destroyAllWindows()
#         break
