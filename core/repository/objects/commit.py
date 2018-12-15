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


class Commit:
    def __init__(self, about: About, id_, parent_id, file_to_storage_name):
        self.__about = about
        self.__file_to_storage_name = file_to_storage_name
        self.__id = id_
        self.__parent_id = parent_id

    @property
    def parent_id(self):
        return self.__parent_id

    @property
    def about(self):
        return self.__about

    @property
    def id(self):
        return self.__id

    def get_file_storage_name(self, file):
        return self.__file_to_storage_name[file]
