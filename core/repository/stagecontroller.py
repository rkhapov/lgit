import os

from core.paths import STAGE_FILE, CONFIG_DIR
from core.repository.path import Path


class StageController:
    def __init__(self, path: Path):
        self.__repo_path = path
        self.__files_at_stage = self._read_files_at_stage()

    def add(self, path, report=False):
        if self.contains(path):
            if report:
                print(f'{path}: already in stage')
            return

        if self.__repo_path.combine(path).startswith(self.__repo_path.combine(CONFIG_DIR)):
            # skip adding config .lgit dir
            return

        if self.__repo_path.isfile(path):
            if report:
                print(f'Added to stage: {path}')
            self.__files_at_stage.add(path)

        if self.__repo_path.isdir(path):
            for f in self.__repo_path.listdir(path):
                self.add(f, report=report)

    def contains(self, path):
        return path in self.__files_at_stage

    def write(self):
        with open(self.__repo_path.combine(STAGE_FILE), 'w') as stage_file:
            for file in self.__files_at_stage:
                stage_file.write(file + os.linesep)

    def get_staged_files(self):
        return self.__files_at_stage

    def _read_files_at_stage(self):
        if not self.__repo_path.isfile(STAGE_FILE):
            return set()

        s = set()

        with open(self.__repo_path.combine(STAGE_FILE), 'r') as stage_file:
            for line in stage_file.readlines():
                s.add(line.strip())

        return s
