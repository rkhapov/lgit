class Author:
    def __init__(self, name, email):
        self.__name = name
        self.__email = email

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email


class About:
    def __init__(self, author: Author, creation_time, comment):
        self.__author = author
        self.__creation_time = creation_time
        self.__comment = comment

    @property
    def comment(self):
        return self.__comment

    @property
    def author(self):
        return self.__author

    @property
    def creation_time(self):
        return self.__creation_time


class Diffs:
    def __init__(self, files_to_store_name, created_dirs, deleted_dirs):
        self.__created_dirs = created_dirs
        self.__deleted_dirs = deleted_dirs
        self.__files_to_storage_name = files_to_store_name

    @property
    def created_dirs(self):
        return self.__created_dirs

    @property
    def deleted_dirs(self):
        return self.__deleted_dirs

    @property
    def files_to_path(self):
        return self.__files_to_storage_name

    def get_file_storage_name(self, path):
        return self.__files_to_storage_name[path]


class Commit:
    def __init__(self, about: About, id_, parent_id, diffs: Diffs):
        self.__about = about
        self.__diffs = diffs
        self.__id = id_
        self.__parent_id = parent_id

    @property
    def parent_id(self):
        return self.__parent_id

    @property
    def about(self):
        return self.__about

    @property
    def diffs(self):
        return self.__diffs

    @property
    def id(self):
        return self.__id
