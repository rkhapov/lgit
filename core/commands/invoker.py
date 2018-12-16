from typing import Dict

from core.commands.add import Add
from core.commands.checkout import Checkout
from core.commands.command import Command
from core.commands.commit import Commit
from core.commands.init import Init
from core.commands.show import Show
from core.commands.status import Status
from core.repository.path import Path


class Invoker:
    __name_to_command: Dict[str, type(Command)] = {
        'init': Init,
        'commit': Commit,
        'add': Add,
        'show': Show,
        'checkout': Checkout,
        'status': Status
    }

    def __init__(self, path: Path):
        self.__path = path

    def invoke(self, cmd: str, args):
        cmd = cmd.lower()

        if cmd not in Invoker.__name_to_command:
            print(f'No that command: {cmd}')
            return

        command = Invoker.__name_to_command[cmd]()

        return command.execute(args, self.__path)
