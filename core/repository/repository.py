from core.repository.path import Path


class Repository:
    def __init__(self, path: Path):
        self.__path = path
        self.__commits = []
        self.__branches = []

    @property
    def path(self):
        return self.__path
