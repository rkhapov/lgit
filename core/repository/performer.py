import shutil

from core.repository.objects.commit import Commit
from core.repository.path import Path
from core.repository.storagecontroller import StorageController


class Performer:
    def __init__(self, path: Path, storage: StorageController):
        self.__repo_path = path
        self.__storage = storage

    def perform_commit(self, commit: Commit):
        self._clear_repo()

        for file, id_ in commit.file_to_storage_name.items():
            path = self.__repo_path.relpath(file)

            self.__repo_path.touch(path)

            shutil.copyfile(self.__storage.get_path_of(id_), path)

    def _clear_repo(self):
        for f in self.__repo_path.listdir('.', full_paths=False):
            if f == '.lgit':
                continue

            self.__repo_path.remove(f)
