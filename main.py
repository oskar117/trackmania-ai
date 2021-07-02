import sys

from ai.commands import Commands, CommandException, Algorithms


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
