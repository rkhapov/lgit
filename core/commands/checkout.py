import argparse

from core.commands.command import Command
from core.repository.objects.provider import Provider
from core.repository.path import Path
from core.repository.repository import contains_repository_at


def _parse_args(args):
    parser = argparse.ArgumentParser(description='Checkout to branch', prog='lgit.py checkout')
    parser.add_argument('name')

    return parser.parse_args(args).name


class Checkout(Command):
    def execute(self, args, path: Path):
        name = _parse_args(args)

        if not contains_repository_at(path):
            print(f'{path.root} doesnt have repository')

        provider = Provider(path)

        if not provider.is_branch(name):
            print(f'Repository doesnt have branch \'{name}\'')
            return

        provider.set_current_branch(name)
        print(f'Current branch for repository was switched to \'{name}\'')