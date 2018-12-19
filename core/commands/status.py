import os

from core.commands.command import Command
from core.repository.path import Path
from core.repository.repository import contains_repository_at, Repository
from core.tools.differ import Differ, State


class Status(Command):
    def execute(self, args, path: Path):
        if not contains_repository_at(path):
            print(f'There is no repository at {path.root}')
            return

        repo = Repository(path)
        branch = repo.provider.get_current_branch()
        current_commit = repo.provider.get_commit(branch.commit_id)
        differ = Differ()
        
        print(f'Repository at branch: {branch.name}')
        file_to_status = differ.get_changes_from_commit(current_commit, repo.storage_controller, repo.path)

        if set(file_to_status.values()) == {State.NOT_CHANGED}:
            print('No any changes in repository')
            return

        def print_for_state(st, intro):
            e = list(map(lambda p: p[0], filter(lambda p: p[1] == st, file_to_status.items())))

            if len(e) == 0:
                return

            print(f'{intro}:{os.linesep}{f"{os.linesep}".join(map(lambda x: " " + x, e))}')

        print_for_state(State.NEW, 'New files')
        print_for_state(State.DELETED, 'Deleted files')
        print_for_state(State.MODIFIED, 'Modified files')
