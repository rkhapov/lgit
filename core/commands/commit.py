from core.commands.command import Command


class Commit(Command):
    def execute(self, args):
        print('i am commit with args:', args)
