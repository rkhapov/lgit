from abc import abstractmethod


class Command:
    @abstractmethod
    def execute(self, args):
        raise NotImplementedError
