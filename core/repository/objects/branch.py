class CommitReference:
    def __init__(self, name: str, commit_id: int):
        self._commit_id = commit_id
        self._name = name

    @property
    def commit_id(self):
        return self._commit_id

    @property
    def name(self):
        return self._name


class Branch(CommitReference):
    def __init__(self, name: str, commit_id: int):
        super().__init__(name, commit_id)

    def set_commit_id(self, new_id):
        self._commit_id = new_id


class Tag(CommitReference):
    def __init__(self, name: str, commit_id: int):
        super().__init__(name, commit_id)
