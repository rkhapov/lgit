from core.commands.command import Command
from core.repository.path import Path


class Commit(Command):
    def execute(self, args, path: Path):
        print('i am commit with args:', args)
