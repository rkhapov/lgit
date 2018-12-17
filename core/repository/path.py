import os
import shutil
from os.path import join, isfile, isdir, dirname, normpath, relpath
from os import makedirs, listdir

from core.paths import CONFIG_DIR


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

    def listdir(self, path, full_paths=True):
        list_ = []

        for f in listdir(self.combine(path)):
            if full_paths:
                list_.append(join(self.combine(path), f))
            else:
                list_.append(f)

        return list_

    def remove(self, path):
        self.remove_file(path)
        self.remove_dir(path)

    def remove_file(self, path):
        if self.isfile(path):
            os.remove(self.combine(path))

    def remove_dir(self, path):
        if self.isdir(path):
            shutil.rmtree(self.combine(path), ignore_errors=True)

    def mkdir(self, path):
        makedirs(join(self.__root, path), exist_ok=True)

    def get_all_files(self, path='.', ignore_config_dir=False):
        result = set()

        self._get_all_files(path, result, ignore_config_dir)

        return result

    def relpath(self, path):
        return normpath(relpath(path, self.__root))

    def _get_all_files(self, path, result, ignore_config_dir):
        if ignore_config_dir and self.combine(path).startswith(self.combine(CONFIG_DIR)):
            return

        if self.isfile(path):
            result.add(path)

        if self.isdir(path):
            for f in self.listdir(path):
                self._get_all_files(f, result, ignore_config_dir)
