import os

from core import paths
from core.repository.branch import Branch
from core.repository.commit import Commit
from core.repository.repository import Repository
from core.tools.storage import deserialize_from_bytes


def build_repository_from(path) -> Repository:
    pass


def build_commit_by_path(path) -> Commit:
    with open(path, 'rb') as about_file:
        return deserialize_from_bytes(about_file.read())


def build_commit_by_id(id_, repository_path):
    return build_commit_by_path(os.path.join(repository_path, paths.COMMITS_DIR_PATH, str(id_)))


def build_branch_by_path(path) -> Branch:
    with open(path, 'rb') as branch_file:
        return deserialize_from_bytes(branch_file.read())


def build_branch_by_name(name, repository_path):
    return build_branch_by_path(os.path.join(repository_path, paths.BRANCHES_DIR_PATH, name))


class _RepositoryBuilder:
    def __init__(self, path):
        self.__path = path
        self.__commits = []
        self.__branches = []

    def build(self) -> Repository:
        return Repository(self.__path, self.__commits, self.__branches)

    def read_commit(self, commit_bytes):
        pass