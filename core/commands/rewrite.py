import argparse

from core.commands.command import Command
from core.repository.objects.provider import Provider
from core.repository.path import Path
from core.repository.repository import contains_repository_at


def _parse_args(args):
    parser = argparse.ArgumentParser(description='Change commit info', usage='lgit rewrite')
    parser.add_argument('-e', '--email', help='New email')
    parser.add_argument('-n', '--name', help='New name')
    parser.add_argument('-c', '--commentary', help='New commentary')
    parser.add_argument("id", help="Commit id to change")

    parsed = parser.parse_args(args)

    return parsed.name, parsed.email, parsed.commentary, parsed.id


class Rewrite(Command):
    def execute(self, args, path: Path):
        if not contains_repository_at(path):
            print(f'There is no repository at {path.root}')
            return

        name, email, comment, id_ = _parse_args(args)
        provider = Provider(path)

        if not provider.is_commit(id_):
            print(f'{id_} is not commit')
            return

        commit = provider.get_commit(id_)

        if name is not None:
            commit.set_author_name(name)

        if email is not None:
            commit.set_author_email(email)

        if comment is not None:
            commit.set_comment(comment)

        provider.save_new(commit)

        print(f'Commit was changed to:')
        print(commit.description_string)
