import time

import cv2
import neat
import pydirectinput
from ai.car import Car
from ai.dataprovider.metadatarecognizer import ImageDataRecognizer, MemoryDataRecognizer, MetaDataRecognizer
from ai.dataprovider.walldetector import WallDetector
from ai.dataprovider.windowcapture import WindowCapture


class Trainer:

    def __init__(self, metadata_recognizer: MetaDataRecognizer) -> None:
        self._wall_detector = WallDetector(700, 700)
        self._window_capture = WindowCapture('TrackMania')
        self._metadata_recognizer = metadata_recognizer
        self.best = (None, -1)

    @property
    def meta_data_recognizer(self):
        return self._metadata_recognizer

    def train(self, genomes, config):
        cars = []
        nets = []
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            cars.append(Car(self._window_capture, self._wall_detector, self._metadata_recognizer))

        for index, car in enumerate(cars):

            gen_time = time.time()
            pydirectinput.press("delete")
            fitness = None
            while time.time() - gen_time < 12:
                metadata, distances = car.drive(nets[cars.index(car)])
                if metadata[1] == 0 and metadata[0] > 20:
                    fitness = 0
                    break
                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                    break
                fitness = self.fitness(metadata)
            genomes[index][1].fitness = fitness
            if fitness > self.best[1]:
                self.best = (nets[cars.index(car)], fitness)

    def fitness(self, metadata: tuple) -> int:
        pass


class VisualTrainer(Trainer):

    def __init__(self):
        super().__init__(ImageDataRecognizer())

    def fitness(self, metadata) -> int:
        return metadata[2]

    def __str__(self) -> str:
        return 'visual'


class MemoryTrainer(Trainer):

    def __init__(self, args):
        super().__init__(MemoryDataRecognizer(args))

    def fitness(self, metadata: tuple) -> int:
        fitness = metadata[2] * 1000
        if metadata[3] == metadata[4]:
            fitness += 10000
        fitness += (100000 - metadata[3]) * metadata[2]
        fitness += metadata[0] * 1000
        return fitness

    def __str__(self) -> str:
        return 'memory'
