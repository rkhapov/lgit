from os.path import join, isfile


class Path:
    def __init__(self, path):
        self.__path = path

    @property
    def path(self):
        return self.__path

    def combine(self, *args):
        return join(self.__path, *args)

    def isfile(self, filename):
        return isfile(join(self.__path, filename))

    def sub(self, path):
        return Path(self.combine(path))
