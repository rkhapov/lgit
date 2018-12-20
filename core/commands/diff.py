import argparse

from core.commands.command import Command
from core.repository.objects.provider import Provider
from core.repository.path import Path
from core.repository.repository import contains_repository_at
from core.repository.storagecontroller import StorageController
from core.tools.differ import Differ, State


def _parse_args(args):
    parser = argparse.ArgumentParser(description='See commits difference', usage='lgit diff')
    parser.add_argument("source", type=int, help="Source commit")
    parser.add_argument("destination", type=int, help="Destination commit")

    parsed = parser.parse_args(args)

    return parsed.source, parsed.destination


class Diff(Command):
    def execute(self, args, path: Path):
        if not contains_repository_at(path):
            print(f'There is no repository at {path.root}')
            return

        src, dst = _parse_args(args)

        provider = Provider(path)
        storage = StorageController(path)

        if not provider.is_commit(src) or not provider.is_commit(dst):
            print('Invalid commit id')
            return

        differ = Differ()
        diffs = differ.get_commit_diffs(provider.get_commit(src), provider.get_commit(dst), storage)

        if len(list(filter(lambda x: x.state == State.DELETED, diffs))) != 0:
            print('Deleted files:')
        for d in filter(lambda x: x.state == State.DELETED, diffs):
            print(d.name)

        if len(list(filter(lambda x: x.state == State.NEW, diffs))) != 0:
            print('New files:')
        for d in filter(lambda x: x.state == State.NEW, diffs):
            print(d.name)

        for d in filter(lambda x: x.state == State.MODIFIED, diffs):
            d.print()
            print('>>>>>>>>>>>>>>>>>>>>>>>>')
