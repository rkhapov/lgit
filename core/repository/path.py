from os.path import join, isfile, isdir
from os import makedirs


class Path:
    def __init__(self, root):
        self.__root = root

    @property
    def root(self):
        return self.__root

    def combine(self, *args):
        return join(self.__root, *args)

    def isfile(self, filename):
        return isfile(join(self.__root, filename))

    def isdir(self, path):
        return isdir(join(self.__root, path))

    def sub(self, path):
        return Path(self.combine(path))

    def mkdir(self, path):
        try:
            makedirs(join(self.__root, path))
        except FileExistsError:
            pass

