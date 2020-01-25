from commands.CommandFactory import CommandFactory
from handlers.Handler import Handler
from parsing.ShellParser import ShellParser


class ParseHandler(Handler):
    def __init__(self, environment):
        super().__init__(environment)
        self.parser = ShellParser(CommandFactory())

    def run(self, input_string):
        result = self.parser.parse(input_string)
        self.on_finish(result)
