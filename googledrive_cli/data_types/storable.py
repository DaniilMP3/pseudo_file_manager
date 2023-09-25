from abc import ABC, abstractmethod
from googledrive_cli.server.db.db import *
from googledrive_cli.exceptions import *


class Storable(ABC):
    def __init__(self, pk: int | None, name: str, parent_id: int = None):
        super().__init__()
        self._pk = pk
        self.name = name
        self._parent_id = parent_id

    @abstractmethod
    def _create(self) -> None:
        pass

    @abstractmethod
    def _is_insertion_available(self) -> bool:
        """
        Checks if storable object can be inserted in hierarchy
        :return: bool
        """
        pass

    def get_children(self) -> list[dict]:
        """
        Get all children of storable if it can have it
        :return: list of children nodes
        """
        pass


class Folder(Storable):
    def __init__(self, name: str, parent_id=None):
        super().__init__(None, name, parent_id)
        if not self._is_insertion_available():
            raise ValueError(f'Cannot create storable object {name}')
        self._create()

    def get_children(self) -> list[dict]:
        res = fetchall("WITH RECURSIVE RecursiveStorage AS ("
                      "SELECT id, name, parent_id FROM storage "
                      "WHERE id = ? "
                      "UNION ALL "
                      "SELECT s.id, s.name, s.parent_id "
                      "FROM storage s "
                      "JOIN RecursiveStorage rs ON s.parent_id = rs.id) "
                      "SELECT id, name, parent_id FROM RecursiveStorage",
                       (self._pk,))
        return res

    def _is_insertion_available(self) -> bool:
        res = fetchall("SELECT name FROM storage WHERE parent_id IS (SELECT parent_id FROM storage WHERE parent_id = ?)", (self._parent_id,))
        return not any(self.name in d.values() for d in res)

    def _create(self, parent_id=None) -> None:
        try:
            execute("INSERT INTO storage VALUES(?, ?, ?, ?) ", (None, self.name, 'folder', parent_id))
        except sqlite3.IntegrityError as e:
            print(f'Cannot create storable object {self.name}')

        self._pk = get_last_rowid()