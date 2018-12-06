#!/usr/bin/env python3
from os import listdir
from os.path import join, isfile, isdir, basename, normpath, realpath
from core.ft.directory import *


def build_directory_from_path(path) -> Directory:
    path = realpath(path)

    if not isdir(path):
        raise NotADirectoryError(f'{path} is not a directory')

    files = list(_get_files_from_path(path))
    subdirs = list(_get_dirs_from_path(path))

    return Directory(basename(normpath(path)), path, subdirs, files)


def _get_files_from_path(path):
    for f in sorted(filter(lambda x: isfile(join(path, x)), listdir(path))):
        yield File(f, join(path, f))


def _get_dirs_from_path(path):
    for d in sorted(filter(lambda x: isdir(join(path, x)), listdir(path))):
        yield build_directory_from_path(join(path, d))
