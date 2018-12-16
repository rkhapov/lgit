from abc import abstractmethod

from core.repository.path import Path


class Command:
    @abstractmethod
    def execute(self, args, path: Path):
        raise NotImplementedError
