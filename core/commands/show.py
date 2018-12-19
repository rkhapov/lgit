import argparse

from core.commands.command import Command
from core.repository.objects.provider import Provider
from core.repository.path import Path
from core.repository.repository import contains_repository_at


def _parse_args(args):
    parser = argparse.ArgumentParser(description='Show branch commits', prog='lgit show')
    parser.add_argument('--branch', type=str, default='', help='branch to show')

    return parser.parse_args(args)


def _print_description(name, provider: Provider):
    print(f'Branch {name}')

    b = provider.get_branch(name)
    commit = provider.get_commit(b.commit_id)

    while True:
        print(commit.description_string)
        print()

        if commit.parent_id < 0:
            break

        commit = provider.get_commit(commit.parent_id)


class Show(Command):
    def execute(self, args, path: Path):
        if not contains_repository_at(path):
            print(f'{path.root} does not contains repository')
            return

        provider = Provider(path)

        args = _parse_args(args)
        branch = args.branch if args.branch != '' else provider.get_current_branch().name

        if not provider.is_branch(branch):
            print(f'No that branch: {branch}')
            return

        _print_description(branch, provider)
