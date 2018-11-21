import sys

from core.selector import build_command_by_name


def main(argv):
    if len(argv) < 2:
        print('Invalid parameters')
        return

    name = argv[1]
    args = argv[2:]

    command = build_command_by_name(name)

    if command is None:
        print('Unknown command')
        return

    command.execute(args)


if __name__ == '__main__':
    main(sys.argv)
