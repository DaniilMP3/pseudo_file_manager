from __future__ import annotations

import re
from typing import Type
from abc import ABC
from file_manager.exceptions import (
    StorableObjectNotExists,
    StorableNameNotAvailable,
    StorableNameAlreadyExists,
)

# Composite Pattern:


def _is_storable_name_available(storable_name: str) -> bool:
    """

    :param storable_name: name of the storable object
    :return: bool
    """
    if not storable_name or not re.match(r"^[A-Za-z0-9_.]+$", storable_name):
        return False
    return True


class StorableComponent(ABC):
    def __init__(self):
        self.parent_directory = None

    def display(self) -> None:
        raise NotImplementedError

    def add(self, new_component: Type[StorableComponent]) -> None:
        raise NotImplementedError

    def remove(self, component: Type[StorableComponent]) -> None:
        raise NotImplementedError

    def get_name(self) -> str:
        raise NotImplementedError

    def get_data(self, *args):
        raise NotImplementedError


class Directory(StorableComponent, ABC):
    def __init__(self, directory_name: str):
        if not _is_storable_name_available(directory_name):
            raise StorableNameNotAvailable(directory_name)
        super().__init__()
        self.storable_objects: list[Type[StorableComponent]] = []
        self._directory_name = directory_name

    def get_name(self) -> str:
        return self._directory_name

    def add(self, new_component: Type[StorableComponent]) -> None:
        if any(
            obj.get_name() == new_component.get_name() for obj in self.storable_objects
        ):
            raise StorableNameAlreadyExists(new_component.get_name())
        new_component.parent_directory = self
        self.storable_objects.append(new_component)

    def remove(self, component: Type[StorableComponent]) -> None:
        for i, obj in enumerate(self.storable_objects):
            if obj.get_name() == component.get_name():
                del self.storable_objects[i]
                break

    def display(self) -> None:
        for storable in self.storable_objects:
            if isinstance(storable, Directory):
                print(storable._directory_name)
            else:
                storable.display()

    def get_data(self):
        return self.storable_objects

    def get_child(self, storable_name: str) -> Type[StorableComponent]:
        for obj in self.storable_objects:
            if obj.get_name() == storable_name:
                return obj
        raise StorableObjectNotExists(storable_name)


class File(StorableComponent):
    def __init__(self, file_name: str):
        if not _is_storable_name_available(file_name):
            raise StorableNameNotAvailable(file_name)
        super().__init__()
        self._file_name = file_name

    def display(self) -> None:
        print(self._file_name)

    def get_name(self) -> str:
        return self._file_name


class Document(File):
    def __init__(self, document_name: str, document_text: str = ""):
        super().__init__(document_name)
        self._document_text = document_text

    def get_data(self):
        return self._document_text

    def display_data(self):
        print(self.get_data())
