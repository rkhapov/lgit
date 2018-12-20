#!/usr/bin/env python3
import enum
from abc import abstractmethod

from core.repository.objects.commit import Commit
from core.repository.path import Path
from core.repository.storagecontroller import StorageController


def _generate_two_dims_arr(val, n, m):
    return [[val for _ in range(m)] for _ in range(n)]


class EditAction:
    @property
    @abstractmethod
    def opposite(self):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError


class EmptyAction(EditAction):
    def __init__(self, position):
        self.__position = position

    @property
    def position(self):
        return self.__position

    @property
    def opposite(self):
        return EmptyAction(self.__position)

    def __eq__(self, other):
        if not other:
            return False

        if not isinstance(other, EmptyAction):
            return False

        return self.position == other.position

    def __str__(self):
        pos = self.__position

        return f'Empty edit action at {pos}'


class Delete(EditAction):
    def __init__(self, position, element):
        self.__position = position
        self.__element = element

    @property
    def position(self):
        return self.__position

    @property
    def element(self):
        return self.__element

    @property
    def opposite(self):
        return Insert(self.__position, self.__element)

    def __str__(self):
        position = self.__position
        element = self.__element

        if isinstance(element, str):
            element = element.replace('\n', '')

        return f'{position}: - "{element}"'

    def __eq__(self, other):
        if not other:
            return False

        if not isinstance(other, Delete):
            return False

        return self.element == other.element and self.position == other.position


class Insert(EditAction):
    def __init__(self, position, element):
        self.__position = position
        self.__element = element

    @property
    def element(self):
        return self.__element

    @property
    def position(self):
        return self.__position

    @property
    def opposite(self):
        return Delete(self.__position, self.__element)

    def __str__(self):
        position = self.__position
        element = self.__element

        if isinstance(element, str):
            element = element.replace('\n', '')

        return f'{position}: + "{element}"'

    def __eq__(self, other):
        if not other:
            return False

        if not isinstance(other, Insert):
            return False

        return self.position == other.position and self.element == other.element


class Replace(EditAction):
    def __init__(self, position, original, substitute):
        self.__position = position
        self.__original = original
        self.__substitute = substitute

    @property
    def position(self):
        return self.__position

    @property
    def original(self):
        return self.__original

    @property
    def substitute(self):
        return self.__substitute

    @property
    def opposite(self):
        return Replace(self.__position, self.__substitute, self.__original)

    def __eq__(self, other):
        if not other:
            return False

        if not isinstance(other, Replace):
            return False

        return self.original == other.original and self.position == other.position and self.substitute == other.substitute

    def __str__(self):
        position = self.__position
        orig = self.__original
        sub = self.__substitute

        if isinstance(orig, str):
            orig = orig.replace('\n', '')
            sub = sub.replace('\n', '')

        return f'{position}: "{orig}" -> "{sub}"'


class State(enum.Enum):
    NEW = 1,
    DELETED = 2,
    MODIFIED = 3,
    NOT_CHANGED = 4


class FileDiff:
    def __init__(self, name, diffs, state):
        self.__name = name
        self.__diffs = diffs
        self.__state = state

    @property
    def state(self):
        return self.__state

    @property
    def name(self):
        return self.__name

    @property
    def diffs(self):
        return self.__diffs

    def print(self):
        if self.state != State.MODIFIED and self.state != State.NEW:
            return

        for act in sorted(self.diffs, key=lambda a: a.position):
            print(act)


class Differ:
    def get_changes_from_commit(self, commit: Commit, storage: StorageController, path: Path):
        file_to_status = {}
        current_files = path.get_all_files(ignore_config_dir=True)

        for file in current_files:
            if not commit.contains_file(file):
                file_to_status[file] = State.NEW
                continue

            id_ = commit.get_file_storage_name(file)

            if self.is_file_differs(file, storage.get_path_of(id_)):
                file_to_status[file] = State.MODIFIED
            else:
                file_to_status[file] = State.NOT_CHANGED

        for cf in commit.file_to_storage_name.keys():
            if cf not in current_files:
                file_to_status[cf] = State.DELETED

        return file_to_status

    def get_commit_diffs(self, src: Commit, dst: Commit, storage: StorageController):
        src_files = set(src.file_to_storage_name.keys())
        dst_files = set(dst.file_to_storage_name.keys())

        fdiffs = []

        for f in src_files.intersection(dst_files):
            diffs = self.get_diff(storage.read_lines_of(src.get_file_storage_name(f)),
                                  storage.read_lines_of(dst.get_file_storage_name(f)))

            fdiffs.append(FileDiff(f, diffs, State.NOT_CHANGED if len(diffs) == 0 else State.MODIFIED))

        fdiffs.extend([FileDiff(f, [], State.DELETED) for f in src_files.difference(dst_files)])
        fdiffs.extend(
            [FileDiff(f,
                      self.get_diff([], storage.read_lines_of(dst.get_file_storage_name(f))),
                      State.NEW) for f in dst_files.difference(src_files)])

        return fdiffs

    def has_difference(self, bytes1, bytes2):
        if len(bytes1) != len(bytes2):
            return True

        for i in range(len(bytes1)):
            if bytes1[i] != bytes2[i]:
                return True

        return False

    def get_file_tree_diff(self, source, destination):
        if source.name != destination.name or source.path != destination.path:
            raise ValueError('cant compare different directories')

        s = {i for i in source.path_tree.split('\n')}
        d = {i for i in destination.path_tree.split('\n')}

        adding = [('+', k) for k in d.difference(s)]
        deleting = [('-', k) for k in s.difference(d)]

        return (*adding, *deleting)

    def is_file_differs(self, path1, path2, size_per_read=1024):
        with open(path1, 'rb') as file1, open(path2, 'rb') as file2:
            while True:
                p1 = file1.read(size_per_read)
                p2 = file2.read(size_per_read)

                if len(p1) != len(p2):
                    return True

                if len(p1) == 0:
                    return False

                if self.has_difference(p1, p2):
                    return True

    def get_diff(self, source, destination, cmp=lambda a, b: a == b):
        m = len(source)
        n = len(destination)

        # dp - minimum edit distance between source and destination dynamic array
        # dp[i][j] - minimum edit distance between prefixes lengths i and j
        dp = _generate_two_dims_arr(-1, m + 1, n + 1)

        # actions[i][j] - chosen edit action at prefixes i, j and indexes of previous action
        actions = _generate_two_dims_arr((None, (-1, -1)), m + 1, n + 1)

        dp[0][0] = 0

        for i in range(1, m + 1):
            dp[i][0] = i
            actions[i][0] = Delete(i - 1, source[i - 1]), (i - 1, 0)

        for j in range(1, n + 1):
            dp[0][j] = j
            actions[0][j] = Insert(0, destination[j - 1]), (0, j - 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                diff = 0 if cmp(source[i - 1], destination[j - 1]) else 1
                dp[i][j] = min((dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + diff))

                if dp[i][j] == dp[i - 1][j] + 1:
                    actions[i][j] = Delete(i - 1, source[i - 1]), (i - 1, j)

                if dp[i][j] == dp[i][j - 1] + 1:
                    actions[i][j] = Insert(i, destination[j - 1]), (i, j - 1)

                if dp[i][j] == dp[i - 1][j - 1] + diff:
                    if diff == 0:
                        actions[i][j] = EmptyAction(i - 1), (i - 1, j - 1)
                    else:
                        actions[i][j] = Replace(i - 1, source[i - 1], destination[j - 1]), (i - 1, j - 1)

        # collecting answer
        acts = []
        curr = actions[m][n]

        while curr[0]:
            acts.append(curr[0])
            curr = actions[curr[1][0]][curr[1][1]]

        return self._count_offsets(filter(lambda a: not isinstance(a, EmptyAction), reversed(acts)))

    def _count_offsets(self, answer):
        insertions_count = 0
        deletions_count = 0

        def travers(a):
            nonlocal insertions_count
            nonlocal deletions_count

            add = insertions_count - deletions_count

            if isinstance(a, Replace):
                return Replace(a.position + add, a.original, a.substitute)

            if isinstance(a, Insert):
                insertions_count += 1
                return Insert(a.position + add, a.element)

            if isinstance(a, Delete):
                deletions_count += 1
                return Delete(a.position + add, a.element)

            raise NotImplementedError

        return list(map(travers, answer))
