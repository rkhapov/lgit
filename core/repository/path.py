from os.path import join, isfile, isdir, dirname, normpath
from os import makedirs, listdir


class Path:
    def __init__(self, root):
        self.__root = root

    @property
    def root(self):
        return self.__root

    def combine(self, *args):
        return normpath(join(self.__root, *args))

    def isfile(self, filename):
        return isfile(self.combine(filename))

    def touch(self, filename):
        if self.isfile(filename):
            return

        dir_ = dirname(filename)

        if not self.isdir(dir_):
            self.mkdir(dir_)

        with open(self.combine(filename), 'wb'):
            pass

    def isdir(self, path):
        return isdir((self.combine(path)))

    def sub(self, path):
        return Path(self.combine(path))

    def exists(self, path):
        return self.isfile(path) or self.isdir(path)

    def listdir(self, path):
        list_ = []

        for f in listdir(self.combine(path)):
            list_.append(join(self.combine(path), f))

        return list_

    def mkdir(self, path):
        try:
            makedirs(join(self.__root, path))
        except FileExistsError:
            pass
