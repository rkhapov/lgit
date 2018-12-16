import argparse
from core.commands.command import Command
from core.repository.path import Path
from core.repository.repository import initialize_repository_at, contains_repository_at


def _parse_args(args):
    parser = argparse.ArgumentParser(description='initializing repository', prog='lgit.py init')
    parser.add_argument('--strict', action='store_true',
                        help='strictly initialize empty repository (in case directory already contains repo)')

    return parser.parse_args(args)


class Init(Command):
    def execute(self, args, path: Path):
        args = _parse_args(args)

        if contains_repository_at(path) and not args.strict:
            print(f'{path.root} already contains repository')
            return

        initialize_repository_at(path)

        print(f'Initialized empty repository at {path.root}')
