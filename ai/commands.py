import pickle
import time

import cv2
import keyboard as keyboard
import neat

from ai.car import Car
from ai.trainer import VisualTrainer, MemoryTrainer, Trainer
from ai.dataprovider.walldetector import WallDetector
from ai.dataprovider.windowcapture import WindowCapture


class Options:

    def __init__(self) -> None:
        self.command_prefix = None

    def to_dict(self) -> dict:
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

    def com_play(self, input_params: str, algorithm: Trainer = None) -> None:
        if algorithm is None:
            raise CommandException("No learning method specified")
        with open(input_params, 'rb') as fp:
            net = pickle.load(fp)
            car = Car(WindowCapture('Trackmania'), WallDetector(700, 700), algorithm.meta_data_recognizer)
            while not keyboard.is_pressed('q'):
                car.drive(net)
        cv2.destroyAllWindows()

    def com_learn(self, input_params: str, algorithm=None) -> None:
        if algorithm is None:
            raise CommandException("No learning method specified")
        population = self.__set_up_neat('config-feedforward.txt')
        print('You have 5 seconds to click on game window!')
        time.sleep(5)
        trainer = algorithm
        best_genome = population.run(trainer.train, 20)
        print(best_genome)
        best_net = trainer.best[0]
        with open(input_params, "wb") as f:
            pickle.dump(best_net, f)

    def com_help(self, input_params: str) -> None:
        print("""
Usage:
    python main.py [learn|play] memory [best_file_name] [game_pid] [speed_addr] [gear_addr]
    [passed_checkpoints_addr] [last_checkpoint_time_addr] [last_lap_time_addr]
OR
    python main.py [learn|play] visual [best_file_name] [path_to_tesseract]
        """),

    def __set_up_neat(self, config_file: str) -> neat.Population:
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

    def alg_visual(self, args: tuple) -> Trainer:
        return VisualTrainer()

    def alg_memory(self, args: tuple) -> Trainer:
        return MemoryTrainer(args)


class CommandException(Exception):
    pass
