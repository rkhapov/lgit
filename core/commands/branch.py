import argparse

from core.commands.command import Command
from core.repository.objects.provider import Provider
from core.repository.objects.branch import Branch as br
from core.repository.path import Path
from core.repository.repository import contains_repository_at


def _parse_args(args):
    parser = argparse.ArgumentParser(description="Branches control of repository", usage='lgit.py branch')
    parser.add_argument('name', help='branch name', nargs='?')
    parser.add_argument('--id', help='id of commit to make branch refer to')
    parser.add_argument('--all', help='show all branches', action='store_true')

    parsed = parser.parse_args(args)

    name = parsed.name
    parsed_id = parsed.id
    parsed_all = parsed.all

    return name, parsed_id, True if name is None else parsed_all


def _create_branch(name, provider):
    if provider.is_branch(name):
        print(f'Branch {name} already exist')
        return

    commit = provider.get_commit(provider.get_current_branch().commit_id).id
    branch = br(name, commit)

    provider.save_new(branch)

    print(f'Created new branch {name} at {commit}')


def _move_branch(name, new_id, provider):
    if not provider.is_branch(name):
        branch = br(name, 0)
        print(f'Created new branch {name}')
    else:
        branch = provider.get_branch(name)

    branch.set_commit_id(new_id)

    provider.save_new(branch)

    print(f'Moved {branch.name} at {new_id}')


def _print_all_branches(provider: Provider):
    for b in provider.get_all_branches():
        print(f'{b.name} -> {b.commit_id}')


class Branch(Command):
    def execute(self, args, path: Path):
        if not contains_repository_at(path):
            print(f'There is not repository at {path.root}')
            return

        name, id_, all_ = _parse_args(args)
        provider = Provider(path)

        if all_:
            _print_all_branches(provider)
            return

        if id_ is None:
            _create_branch(name, provider)
        else:
            _move_branch(name, id_, provider)
