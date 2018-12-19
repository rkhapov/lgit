import argparse
import datetime

from core.commands.command import Command
from core.repository.objects.commit import About, Author, Commit as cm
from core.repository.objects.provider import Provider
from core.repository.path import Path
from core.repository.repository import contains_repository_at
from core.repository.stagecontroller import StageController
from core.repository.storagecontroller import StorageController
from core.tools.differ import Differ, State


def _parse_about(args):
    parser = argparse.ArgumentParser(description='Commit stage', prog='lgit commit')
    parser.add_argument('-c', '--comment', type=str, help='Commentary to the commit', required=True)
    parser.add_argument('-n', '--name', type=str, help='Name of author', required=True)
    parser.add_argument('-e', '--email', type=str, help='Email of author', required=True)

    parsed = parser.parse_args(args)

    return About(Author(parsed.name, parsed.email), datetime.datetime.now(), parsed.comment)


class Commit(Command):
    def execute(self, args, path: Path):
        if not contains_repository_at(path):
            print(f'There is no repository at {path.root}')
            return

        about = _parse_about(args)

        provider = Provider(path)
        storage = StorageController(path)
        stage = StageController(path)
        differ = Differ()
        branch = provider.get_current_branch()
        commit = provider.get_commit(branch.commit_id)

        if stage.is_empty():
            print('Nothing to commit: stage is empty')
            return

        changes = differ.get_changes_from_commit(commit, storage, path)
        file_to_id = {}

        for f, s in changes.items():
            if not stage.contains(f):
                continue

            if s == State.NOT_CHANGED:
                file_to_id[f] = commit.get_file_storage_name(f)
            elif s == State.NEW or s == State.MODIFIED:
                print(f'Commit {f}')
                file_to_id[f] = storage.save_file(f)
            # deleted files are not saved in commit

        id_ = provider.get_next_commit_id()

        new_commit = cm(about, id_, commit.id, file_to_id)
        branch.set_commit_id(id_)

        provider.save_new(new_commit)
        provider.save_new(branch)

        print(new_commit.description_string)

        stage.clear()
        stage.write()


