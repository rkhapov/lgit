import argparse

from core.commands.command import Command
from core.repository.path import Path
from core.repository.repository import contains_repository_at
from core.repository.stagecontroller import StageController


def _parse_args(args):
    parse = argparse.ArgumentParser(description='Add files to stage', prog='lgit.py add')
    parse.add_argument('file', nargs='+', help='files or directories for pushing to stage')

    return parse.parse_args(args)


class Add(Command):
    def execute(self, args, path: Path):
        args = _parse_args(args)

        if not contains_repository_at(path):
            print(f'No repository at {path.root}')
            return

        con = StageController(path)

        for file in args.file:
            if not path.exists(file):
                print(f'No that file or directory: {file}')

            con.add(file, report=True)

        con.write()
