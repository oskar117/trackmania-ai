import time

import neat

from trainer import VisualTrainer


class Commands:

    def __init__(self):
        self._command_prefix = 'com_'

    def to_dict(self):
        result = {}
        for command_name in dir(self):
            if not command_name.startswith(self._command_prefix):
                continue
            method = getattr(self, command_name)
            result[command_name[len(self._command_prefix):]] = method
        return result

    def com_play(self, input_params):
        print('play!')

    def com_learn(self, input_params):
        print('learn!')
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, 'config-feedforward.txt')
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        time.sleep(5)
        trainer = VisualTrainer()
        p.run(trainer.train, 50)


class CommandException(Exception):
    pass
