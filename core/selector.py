from core.commit import Commit
from core.init import Init

_name_to_command = {
    'init': Init,
    'commit': Commit
}


def build_command_by_name(name):
    if name in _name_to_command:
        return _name_to_command[name]()

    return None
