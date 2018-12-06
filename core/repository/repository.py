from typing import List, Dict
from core.repository.commit import Commit
from core.repository.branch import Branch
import os


class Repository:
    def __init__(self, path: str, commits: List[Commit], branches: List[Branch]):
        self.__path = path
        self.__id_to_commit: Dict[int, Commit] = {c.id: c for c in commits}
        self.__branches = branches

    @property
    def path(self):
        return self.__path

    @property
    def commits(self):
        return self.__id_to_commit.values()

    @property
    def branches(self):
        return self.__branches

    def get_commit_by_id(self, id_):
        return self.__id_to_commit[id_]

    def get_commit_dir(self, commit: Commit):
        return os.path.join(self.__path, "commits", commit.id)
