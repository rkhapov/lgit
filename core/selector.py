from typing import Dict
from core.commands.command import Command
from core.commands.commit import Commit
from core.commands.init import Init

_name_to_command: Dict[str, type(Command)] = {
    'init': Init,
    'commit': Commit
}


def build_command_by_name(name) -> [Command, None]:
    if name in _name_to_command:
        return _name_to_command[name]()

    return None
