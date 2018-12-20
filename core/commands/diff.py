import argparse
from os.path import normpath

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
    parser.add_argument('-f', '--file', type=str, help='file to see diffs')

    parsed = parser.parse_args(args)

    return parsed.source, parsed.destination, parsed.file


class Diff(Command):
    def execute(self, args, path: Path):
        if not contains_repository_at(path):
            print(f'There is no repository at {path.root}')
            return

        src, dst, file = _parse_args(args)

        provider = Provider(path)
        storage = StorageController(path)

        if not provider.is_commit(src) or not provider.is_commit(dst):
            print('Invalid commit id')
            return

        differ = Differ()
        diffs = differ.get_commit_diffs(provider.get_commit(src), provider.get_commit(dst), storage)

        if file is not None:
            print(f'Diffs at file {file}:')

            for d in diffs:
                if path.relpath(d.name) != normpath(file):
                    continue

                if d.state == State.DELETED:
                    print('File was deleted')
                elif d.state == State.NOT_CHANGED:
                    print('File didnt changed')
                else:
                    d.print()
                break
        else:
            def print_(t, p, m):
                l = list(filter(lambda x: x.state == t, p))

                if len(l) == 0:
                    return

                print(m)
                for d in l:
                    print(d.name)

            print_(State.DELETED, diffs, 'Deleted files')
            print_(State.NEW, diffs, 'New files')
            print_(State.MODIFIED, diffs, 'Modified files')
