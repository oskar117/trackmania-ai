import pickle
import time

import cv2
import keyboard as keyboard
import neat

from car import Car
from trainer import VisualTrainer, MemoryTrainer, Trainer
from dataprovider.walldetector import WallDetector
from dataprovider.windowcapture import WindowCapture


class Options:

    def __init__(self):
        self.command_prefix = None

    def to_dict(self):
        result = {}
        for command_name in dir(self):
            if not command_name.startswith(self.command_prefix):
                continue
            method = getattr(self, command_name)
            result[command_name[len(self.command_prefix):]] = method
        return result


class Commands(Options):

    def __init__(self):
        super().__init__()
        self.command_prefix = 'com_'

    def com_play(self, input_params, algorithm: Trainer = None):
        if algorithm is None:
            raise CommandException("No learning method specified")
        with open(input_params, 'rb') as fp:
            net = pickle.load(fp)
            car = Car(WindowCapture('Trackmania'), WallDetector(700, 700), algorithm.meta_data_recognizer)
            while not keyboard.is_pressed('q'):
                car.drive(net)
        cv2.destroyAllWindows()

    def com_learn(self, input_params, algorithm=None):
        if algorithm is None:
            raise CommandException("No learning method specified")
        population = self.__set_up_neat('config-feedforward.txt')
        print('You have 5 seconds to click on game window!')
        time.sleep(5)
        trainer = algorithm
        best_genome = population.run(trainer.train, 1)
        print(best_genome)
        best_net = trainer.best[0]
        with open(input_params, "wb") as f:
            pickle.dump(best_net, f)

    def com_help(self, input_params):
        print("help"),

    def __set_up_neat(self, config_file) -> neat.Population:
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_file)
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        return p


class Algorithms(Options):

    def __init__(self) -> None:
        super().__init__()
        self.command_prefix = 'alg_'

    def alg_visual(self, args):
        return VisualTrainer()

    def alg_memory(self, args):
        return MemoryTrainer(args)


class CommandException(Exception):
    pass
