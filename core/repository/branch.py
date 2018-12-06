from core.repository.commit import Commit


class Branch:
    def __init__(self, name: str, commit: Commit, is_static=False):
        self.__commit = commit
        self.__name = name
        self.__is_static = is_static

    @property
    def is_static(self):
        return self.__is_static

    @property
    def commit(self):
        return self.__commit

    @property
    def name(self):
        return self.__name
