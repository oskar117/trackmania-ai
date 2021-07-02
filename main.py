import sys

from ai.commands import Commands, CommandException, Algorithms


# wincap = WindowCapture('TrackMania')
# mdr = MetaDataRecognizer()
#
# wall_detector = WallDetector(700, 700)
#
#
# # loop_time = time()
# # print('lap time: ',  readmemory.GetSpeed(0x00001CD8, 0x7FF6E95DCA04))
# # print('last checkpoint: ',  readmemory.GetSpeed(0x00001CD8, 0x26EBC5B0C98))
# # print('final_lap_time: ',  readmemory.GetSpeed(0x00001CD8, 0x26F57D40E78))
# # print('speed: ', readmemory.GetSpeed(0x00002854, 0x26F57826F98))
#
# def run_learning(genomes, config):
#     cars = []
#     nets = []
#     for genome_id, genome in genomes:
#         genome.fitness = 0
#         net = neat.nn.FeedForwardNetwork.create(genome, config)
#         nets.append(net)
#         cars.append(Car())
#
#     for index, car in enumerate(cars):
#
#         gen_time = time.time()
#         distance_travelled = 0,
#         pydirectinput.press('delete')
#         while time.time() - gen_time < 20:
#             distance_travelled, speed = process_car(nets[cars.index(car)], car)
#             if speed < -20:
#                 break
#             if cv2.waitKey(1) == ord('q'):
#                 cv2.destroyAllWindows()
#                 break
#         genomes[index][1].fitness = distance_travelled
#
#
# def process_car(net, car):
#     i = wincap.get_screenshot()
#     distances = wall_detector.calculate_distances(i)
#     gear, speed, distance = mdr.extract_data(i)
#     output = net.activate(distances + (gear, speed, distance))
#     car.drive(output)
#     return distance, speed
#
#
# config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
#                             neat.DefaultStagnation, 'config-feedforward.txt')
#
# p = neat.Population(config)
#
# p.add_reporter(neat.StdOutReporter(True))
# stats = neat.StatisticsReporter()
# p.add_reporter(stats)
# time.sleep(5)
# p.run(run_learning, 50)
# while True:
#     i = wincap.get_screenshot()
#     distances = wall_detector.calculate_distances(i)
#
#     gear, speed, distance = mdr.extract_data(i)
#     print(gear, speed, distance)
#     if cv2.waitKey(1) == ord('q'):
#         cv2.destroyAllWindows()
#         break


class Main:

    def __init__(self) -> None:
        self.command_dict = Commands().to_dict()
        self.algorithm_dict = Algorithms().to_dict()

    def run(self):
        cmd, *input_args = sys.argv[1:]
        if not cmd:
            print("No parameters given")
        else:
            if cmd in self.command_dict:
                try:
                    alg_instance = None
                    try:
                        alg_instance = self.algorithm_dict[input_args[0]](input_args[2:])
                    except IndexError:
                        pass
                    self.command_dict[cmd](input_args[1], algorithm=alg_instance)
                except CommandException as e:
                    print(e, file=sys.stderr)
            else:
                print(f"Command '{cmd}' not found")


if __name__ == "__main__":
    main = Main()
    main.run()
