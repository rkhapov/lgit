import shutil
import uuid

from core.paths import STORAGE_PATH
from core.repository.path import Path


class Storage:
    def __init__(self, repository_path: Path):
        self.__repository_path = repository_path
        self.__storage_path = repository_path.sub(STORAGE_PATH)

    @property
    def repository_path(self):
        return self.__repository_path

    @property
    def storage_path(self):
        return self.__storage_path

    def save(self, *args, path=None, bytes_=None) -> str:
        if path is None and bytes_ is None or path is not None and bytes_ is not None:
            raise ValueError('one of path or bytes should be presented')

        if path is not None:
            return self.save_file(path)

        return self.save_bytes(bytes_)

    def save_bytes(self, bytes_):
        id_ = self._get_id()

        with open(self.__storage_path.combine(id_), 'wb') as file:
            file.write(bytes_)

        return id_

    def save_file(self, path) -> str:
        id_ = self._get_id()

        shutil.copyfile(self.__repository_path.combine(path), self.__storage_path.combine(id_))

        return id_

    def read_bytes_of(self, id_):
        path = self.__storage_path.combine(id_)
        bytes_ = bytearray()

        with open(path, 'rb') as file:
            while True:
                part = file.read(16 * 1024)  # 16KB

                if len(part) == 0:
                    break

                bytes_.extend(path)

        return bytes_

    def get_file_of(self, id_, mode='rb'):
        path = self.__storage_path.combine(id_)

        return open(path, mode=mode)

    def get_path_of(self, id_):
        return self.__storage_path.combine(id_)

    def _get_id(self) -> str:
        times = 0
        id_ = str(uuid.uuid4())

        while self.__storage_path.isfile(id_):
            id_ = str(uuid.uuid4())
            times += 1

            if times > 1000:
                raise RuntimeError("Cant get id for storage")

        return id_
