#!/usr/bin/env python3
import os


class File:
    def __init__(self, name, path):
        self.__name = name
        self.__path = path

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    def get_content(self, mode='r', length=-1):
        if mode != 'r' and mode != 'rb':
            raise ValueError('expected r or rb mode to get file content')

        with open(self.path, mode) as file:
            return file.read(length)

    def __str__(self):
        return f'File {self.path}'


class Directory:
    def __init__(self, name, path, subdirs, files):
        self.__name = name
        self.__subdirs = tuple(sorted(subdirs, key=lambda x: x.name))
        self.__path = path
        self.__files = files

    @property
    def files(self):
        return self.__files

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def subdirs(self):
        return self.__subdirs

    @property
    def path_tree(self):
        result = ''

        def visitor(ch):
            nonlocal result
            result += ch.path + os.linesep

        self.traverse_tree(visitor)

        return result

    def traverse_tree(self, visitor):

        for f in self.files:
            visitor(f)

        for ch in self.subdirs:
            visitor(ch)
            ch.traverse_tree(visitor)

    def select_child_by_path(self, path):
        current = self
        tokens = path.split(os.sep)

        for t in tokens[:-1]:
            if t == '.':
                continue

            if t == '..':
                raise ValueError(f'Cant go to parent. Path = {path}')

            current = current.select_subdir(t)

        return current.select_child(tokens[-1])

    def select_child(self, name):
        child = self.try_get_child(name)

        if child is None:
            raise LookupError(f'No such child: {name}')

        return child

    def try_get_child(self, name):
        as_file = self.try_get_file(name)
        as_dir = self.try_get_subdir(name)

        if as_file is not None:
            return as_file

        if as_dir is not None:
            return as_dir

        return None

    def select_subdir(self, name):
        d = self.try_get_subdir(name)

        if d in None:
            raise LookupError(f'No that subdir: {name}')

        return d

    def select_file(self, name):
        f = self.try_get_file(name)

        if f is None:
            raise LookupError(f'No such file: {name}')

        return f

    def try_get_file(self, name):
        for f in self.__files:
            if f.name == name:
                return f

        return None

    def try_get_subdir(self, name):
        for d in self.subdirs:
            if d.name == name:
                return d

        return None

    def __str__(self):
        return f'Directory {self.path}'
