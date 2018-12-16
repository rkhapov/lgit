from core.commands.command import Command
from core.repository.objects.provider import Provider
from core.repository.path import Path
from core.repository.repository import contains_repository_at
from core.repository.stagecontroller import StageController
from core.repository.storagecontroller import StorageController
from core.tools.differ import Differ, State


class Commit(Command):
    def execute(self, args, path: Path):
        if not contains_repository_at(path):
            print(f'There is no repository at {path.root}')
            return

        provider = Provider(path)
        storage = StorageController(path)
        stage = StageController(path)
        differ = Differ()
        branch = provider.get_current_branch()
        commit = provider.get_commit(branch.commit_id)

        files_to_commit = stage.get_staged_files()
        changes = differ.get_changes_from_commit(commit, storage, path)

        for f in files_to_commit:
            if changes[f] == State.NOT_CHANGED:
                print(f'Staged file {f} skipped: not changed')
                continue


