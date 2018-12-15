from abc import abstractmethod

from core.repository.repository import Repository


class Command:
    @abstractmethod
    def execute(self, args, repository: Repository) -> Repository:
        raise NotImplementedError
