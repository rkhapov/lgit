from core.commands.command import Command


class Init(Command):
    def execute(self, args):
        print('i am init with args:', args)
