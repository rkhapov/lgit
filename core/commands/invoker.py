from typing import Dict
from core.commands.command import Command
from core.commands.commit import Commit
from core.commands.show import Show
from core.commands.add import Add
from core.commands.init import Init
from core.repository.repository import Repository


class Invoker:
    __name_to_command: Dict[str, type(Command)] = {
        'init': Init,
        'commit': Commit,
        'add': Add,
        'show': Show
    }

    def __init__(self, repository: Repository):
        self.__repository = repository

    def invoke(self, cmd: str, args) -> Repository:
        cmd = cmd.lower()

        if cmd not in Invoker.__name_to_command:
            return None

        command = Invoker.__name_to_command[cmd]()

        return command.execute(args, self.__repository)
