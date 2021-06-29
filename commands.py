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


class CommandException(Exception):
    pass
