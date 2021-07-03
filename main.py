import sys

from ai.commands import Commands, CommandException, Algorithms


class Main:

    def __init__(self) -> None:
        self.command_dict = Commands().to_dict()
        self.algorithm_dict = Algorithms().to_dict()

    def run(self):
        if len(sys.argv) < 2:
            print("No parameters given")
            self.command_dict['help'](None)
        else:
            cmd, *input_args = sys.argv[1:]
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
                self.command_dict['help'](None)


if __name__ == "__main__":
    main = Main()
    main.run()
