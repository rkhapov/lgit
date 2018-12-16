import datetime
import shutil

from core.paths import *
from core.repository.objects.branch import Branch
from core.repository.objects.commit import About, Author, Commit
from core.repository.objects.provider import Provider
from core.repository.path import Path
from core.repository.storagecontroller import StorageController


def initialize_repository_at(path: Path):
    if path.isdir(CONFIG_DIR):
        shutil.rmtree(path.combine(CONFIG_DIR))

    path.mkdir(COMMITS_DIR)
    path.mkdir(BRANCHES_DIR)
    path.mkdir(STORAGE_PATH)

    provider = Provider(path)
    commit = Commit(About(Author('N\\A', 'N\\A'), datetime.datetime.now(), 'lgit auto initialization commit'), 0, -1, {})
    master = Branch('master', 0)
    provider.save_new(commit)
    provider.save_new(master)
    provider.set_current_branch('master')


def contains_repository_at(path: Path):
    return path.isdir(COMMITS_DIR) and\
           path.isdir(BRANCHES_DIR) and\
           path.isdir(STORAGE_PATH) and\
           path.isfile(CURRENT_BRANCH_FILE)


class Repository:
    def __init__(self, path: Path):
        self.__path = path
        self.__provider = Provider(path)
        self.__storage = StorageController(path)

    @property
    def path(self):
        return self.__path

    @property
    def provider(self):
        return self.__provider

    @property
    def storage_controller(self):
        return self.__storage
