import io
import logging
import subprocess
from typing import Union

from commands.Command import Command


class CustomCommand(Command):
    """
    Custom command is used when no build-in command found.
    Command name is being found in file system and in PATH.
    """

    def execute(self, input_stream: io.StringIO, output_stream: io.StringIO) -> int:
        name, args = self.args[0], self.args[1:]
        logging.debug("[CustomCommand, %s] args = %s", name, str(args))
        command = self.which(name)
        if command is None:
            logging.error('Unknown command %s', name)
            return 1
        else:
            process = subprocess.Popen([command] + args, universal_newlines=True,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out_str, err_str) = process.communicate(input_stream.getvalue())
            output_stream.write(out_str)
            if len(err_str) > 0:
                logging.error("[Custom command, %s] %s", name, err_str)
            return process.returncode

    def which(self, program: str) -> Union[str, None]:
        """Finds executable file in file system and in PATH."""
        import os

        def is_exe(file: str) -> bool:
            return os.path.isfile(file) and os.access(file, os.X_OK)

        file_path, file_name = os.path.split(program)
        if file_path:
            if is_exe(program):
                return program
        else:
            for path in self.environment.get('PATH').split(os.pathsep):
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None
