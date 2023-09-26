import sqlite3
from abc import ABC, abstractmethod
from googledrive_cli.server.db.db import *
from googledrive_cli.exceptions import *


class Storable(ABC):
    def __init__(self, name: str, storable_tag: str):
        self._pk = None
        self._name = name
        self._storable_tag = storable_tag

    @abstractmethod
    def _create(self) -> None:
        pass

    @abstractmethod
    def _is_insertion_available(self) -> bool:
        """
        Checks if storable object can be inserted in hierarchy
        :return: True if storable object can be inserted, else: False
        """

    @abstractmethod
    def _already_exists(self) -> bool:
        """
        Checks if object is already existed in database
        """


class Directory(Storable):
    def __init__(self, name: str, parent_id: int = None):
        super().__init__(name, 'directory')
        self._parent_directory_id = parent_id
        if self._already_exists():
            raise ValueError(f'Directory with name: {name} already existed')
        if not self._is_insertion_available():
            raise ValueError(f'Cannot create directory with the name: {name}')
        self._create()

    def _create(self) -> None:
        try:
            execute("INSERT INTO directory VALUES(?, ?, ?)", (None, self._parent_directory_id, self._name))
        except sqlite3.IntegrityError as e:
            print(f'Cannot create with the name: {self._name}')
        self._pk = get_last_rowid()

    def _is_insertion_available(self) -> bool:
        res = fetchall(
            "SELECT directory_name FROM directory WHERE parent_directory IS (SELECT parent_directory FROM directory WHERE parent_directory = ?)",
            (self._parent_directory_id,))
        if res is None:
            return True
        return not any(self._name in d.values() for d in res)

    def _already_exists(self) -> bool:
        res = fetchone("SELECT id FROM directory WHERE directory_name = ? AND parent_directory IS ?",
                       (self._name, self._parent_directory_id))
        return bool(res)

    def get_children(self):
        res = fetchall("WITH RECURSIVE RecursiveDirectory AS ("
                       "SELECT id, directory_name, parent_directory FROM directory "
                       "WHERE id = ? "
                       "UNION ALL "
                       "SELECT d.id, d.directory_name, d.parent_directory "
                       "FROM directory d "
                       "JOIN RecursiveDirectory rd ON d.parent_directory = rd.id) "
                       "SELECT id, directory_name, parent_directory FROM RecursiveDirectory "
                       "UNION "
                       "SELECT f.id, f.file_name FROM file f "
                       "WHERE f.fk_directory = ?",
                       (self._pk, self._pk))
        return res


#
#
# class Directory(ABC, Storable):
#     def __init__(self, name: str, parent_id: int = None):
#         super().__init__(name, parent_id)
#
#     def get_children(self) -> list[dict]:
#         res = fetchall("WITH RECURSIVE RecursiveStorage AS ("
#                        "SELECT id, name, parent_id FROM storage "
#                        "WHERE id = ? "
#                        "UNION ALL "
#                        "SELECT s.id, s.name, s.parent_id "
#                        "FROM storage s "
#                        "JOIN RecursiveStorage rs ON s.parent_id = rs.id) "
#                        "SELECT id, name, parent_id FROM RecursiveStorage",
#                        (self._pk,))
#         return res
#
#
# class TextStorable(ABC, Storable):
#     def __init__(self, name: str, parent_id: int = None):
#         super().__init__(name, parent_id)
#
#
#
# class Folder(StorableDirectory):
#     def __init__(self, name: str, parent_id=None):
#         super().__init__(name, parent_id)
#         if not self._is_insertion_available():
#             raise ValueError(f'Cannot create file {name}')
#         self._create()
#
#     def _create(self) -> None:
#         try:
#             execute("INSERT INTO storage VALUES(?, ?, ?, ?) ", (None, self.name, 'folder', self._parent_id))
#         except sqlite3.IntegrityError as e:
#             print(f'Cannot create folder {self.name}')
#
#         self._pk = get_last_rowid()
#
#
# class Document(Storable):
#     def __init__(self, name: str, text: str, parent_id: int = None):
#         super().__init__(name, parent_id)
#         if not self._is_insertion_available():
#             raise ValueError(f'Cannot create document {name}')
#         self.text = text
#         self._create()
#
#     def _create(self) -> None:
#         try:
#             execute("INSERT INTO storage VALUES(?, ?, ?, ?)", (None, self.name, 'file', self._parent_id))
#         except sqlite3.IntegrityError as e:
#             print(f'Cannot create file {self.name}')
#
#         self._pk = get_last_rowid()

