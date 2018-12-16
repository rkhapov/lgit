import os
import sys
from core.commands.invoker import Invoker
from core.repository.path import Path


def main(argv):
    if len(argv) < 2:
        print('Invalid parameters: expected command name')
        return

    name = argv[1]
    args = argv[2:]
    path = Path(os.getcwd())
    invoker = Invoker(path)

    invoker.invoke(name, args)


if __name__ == '__main__':
    main(sys.argv)
