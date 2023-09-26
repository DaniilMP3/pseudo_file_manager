from __future__ import annotations
from typing import Type
import sqlite3
from abc import ABC, abstractmethod
from googledrive_cli.server.db.db import *
from googledrive_cli.exceptions import *


class StorableComponent(ABC):
    def remove(self, component: StorableComponent) -> None:
        raise NotImplementedError
    #


    def display(self):
        raise NotImplementedError


class Directory(StorableComponent):
    def __init__(self, directory_name: str):
        self.storable_objects: list[Type[StorableComponent]] = []
        self.directory_name = directory_name

    def add(self, new_component: type[StorableComponent]) -> None:
        self.storable_objects.append(new_component)

    def display(self):
        for storable in self.storable_objects:
            storable.display()


class File(StorableComponent):
    def __init__(self, file_name: str):
        self.file_name = file_name




# class Storable(ABC):
#     def __init__(self, name: str, parent_directory_id: int = None):
#         self._pk = None
#         self._name = name
#         self._parent_directory_id = parent_directory_id
#
#     @abstractmethod
#     def _create(self) -> None:
#         pass
#
#     @abstractmethod
#     def _is_insertion_available(self) -> bool:
#         """
#         Checks if storable object can be inserted in hierarchy
#         :return: True if storable object can be inserted, else: False
#         """
#
#     @abstractmethod
#     def _already_exists(self) -> bool:
#         """
#         Checks if object is already existed in database
#         """
#
#
# class Directory(Storable):
#     def __init__(self, name: str, parent_directory_id: int = None):
#         super().__init__(name, parent_directory_id)
#         if self._already_exists():
#             raise ValueError(f'Directory with name: {name} already exists')
#         if not self._is_insertion_available():
#             raise ValueError(f'Cannot create directory with the name: {name}')
#         self._create()
#
#     def _create(self) -> None:
#         try:
#             execute("INSERT INTO directory VALUES(?, ?, ?)", (None, self._parent_directory_id, self._name))
#         except sqlite3.IntegrityError as e:
#             print(f'Cannot create with the name: {self._name}')
#         self._pk = get_last_rowid()
#
#     def _is_insertion_available(self) -> bool:
#         res = fetchone(
#             "SELECT directory_name FROM directory WHERE parent_directory IS (SELECT parent_directory FROM directory WHERE parent_directory = ?)",
#             (self._parent_directory_id,))
#         if res is None:
#             return True
#         return not any(self._name in d.values() for d in res)
#
#     def _already_exists(self) -> bool:
#         res = fetchone("SELECT id FROM directory WHERE directory_name = ? AND parent_directory IS ?",
#                        (self._name, self._parent_directory_id))
#         return bool(res)
#
#     def get_children(self):
#         res = fetchall("WITH RECURSIVE RecursiveDirectory AS ("
#                        "SELECT id, directory_name, parent_directory FROM directory "
#                        "WHERE id = ? "
#                        "UNION ALL "
#                        "SELECT d.id, d.directory_name, d.parent_directory "
#                        "FROM directory d "
#                        "JOIN RecursiveDirectory rd ON d.parent_directory = rd.id) "
#                        "SELECT id, directory_name, parent_directory FROM RecursiveDirectory "
#                        "UNION "
#                        "SELECT f.id, f.file_name FROM file f "
#                        "WHERE f.fk_directory = ?",
#                        (self._pk, self._pk))
#         return res
#
#
# class FileStorable(Storable, ABC):
#     def __init__(self, name: str, parent_directory_id: int = None):
#         super(Storable).__init__(name, parent_directory_id)
#         execute("INSERT INTO file VALUES(?, ?, ?)", (None, self._parent_directory_id, self._name))
#         self._file_pk = get_last_rowid()
#
#     def _is_insertion_available(self) -> bool:
#         res = fetchone("SELECT file_name FROM file WHERE file_name = ? AND fk_directory IS ?",
#                        (self._name, self._parent_directory_id))
#         if res is None:
#             return True
#         return not any(self._name in d.values() for d in res)
#
#     def _already_exists(self) -> bool:
#         res = fetchone("SELECT id FROM file WHERE id = ? AND fk_directory IS ?", (self._file_pk, self._parent_directory_id))
#         return bool(res)
#
# class Document(FileStorable):
#     def __init__(self, name: str, text: str, parent_directory_id: int = None):
#         super().__init__(name, parent_directory_id)
#         self.text = text
#
#     def _create(self) -> None:
#         try:
#             execute("INSERT INTO file_document VALUES(?, ?, ?)", (None, self.text, self._file_pk))
#         except sqlite3.IntegrityError as e:
#             print(f'Cannot create document {self._name}')
#         self._pk = get_last_rowid()
