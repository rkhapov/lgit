from os import listdir
from os.path import join

from core.repository.objects.branch import Branch
from core.repository.objects.commit import Commit
from core.repository.path import Path
from core.tools.converters import deserialize_from_bytes, serialize_to_bytes

OBJECTS_DIR = join(".lgit", "objects")
COMMITS_DIR = join(OBJECTS_DIR, "commits")
BRANCHES_DIR = join(OBJECTS_DIR, "branches")
CURRENT_BRANCH_FILE = join(OBJECTS_DIR, "CURRENT_BRANCH")


class CommitProvider:
    def __init__(self, path: Path):
        self.__path = path

    def load(self, id_):
        with open(self.__path.combine(str(id_)), 'rb') as commit_file:
            return deserialize_from_bytes(commit_file.read())

    def load_all(self):
        commits = []

        for id_ in filter(lambda x: x.isnumeric() and self.__path.isfile(id_), listdir(self.__path.path)):
            commits.append(self.load(id_))

        return commits

    def save_new(self, commit: Commit):
        with open(self.__path.combine(str(commit.id)), 'wb') as commit_file:
            commit_file.write(serialize_to_bytes(commit))


class BranchProvider:
    def __init__(self, path: Path):
        self.__path = path

    def load(self, name):
        with open(self.__path.combine(name), 'rb') as branch_file:
            return deserialize_from_bytes(branch_file.read())

    def load_all(self):
        branches = []

        for name in filter(lambda x: self.__path.isfile(x), listdir(self.__path.path)):
            branches.append(self.load(name))

        return branches

    def save_new(self, branch: Branch):
        with open(self.__path.combine(branch.name), 'wb') as commit_file:
            commit_file.write(serialize_to_bytes(branch))


class Provider:
    def __init__(self, repository_path: Path):
        self.__repository_path = repository_path
        self.__commit_provider = CommitProvider(repository_path.sub(COMMITS_DIR))
        self.__branch_provider = BranchProvider(repository_path.sub(BRANCHES_DIR))

    def get_commit(self, id_):
        return self.__commit_provider.load(id_)

    def get_branch(self, name):
        return self.__branch_provider.load(name)

    def get_all_branches(self):
        return self.__branch_provider.load_all()

    def get_all_commits(self):
        return self.__commit_provider.load_all()

    def save_new(self, object_):
        if isinstance(object_, Commit):
            self.__commit_provider.save_new(object_)

        if isinstance(object_, Branch):
            self.__branch_provider.save_new(object_)

    def set_current_branch(self, name):
        with open(self.__repository_path.combine(CURRENT_BRANCH_FILE), 'w') as file:
            file.write(name)

    def get_current_branch(self) -> Branch:
        with open(self.__repository_path.combine(CURRENT_BRANCH_FILE), 'r') as file:
            name = file.readline().strip()

        return self.__branch_provider.load(name)
