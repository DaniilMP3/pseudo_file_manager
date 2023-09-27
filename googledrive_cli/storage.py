from googledrive_cli.data_types.storable import Directory, Document, StorableComponent
from abc import ABC
from googledrive_cli.exceptions import *


def _pre_process_file_path(file_path: str) -> str:
    flag = False
    for i, char in enumerate(file_path):
        if char in '\\':  # Unavailable separator
            return ''
        if char == '/' and flag:
            file_path = file_path[:i] + file_path[i + 1:]  # Remove extra '/'
        elif char == '/' and not flag:
            flag = True


def _is_file_path_correct(file_path: str, ) -> bool:
    if not file_path:
        return False
    pass


class CloudStorage(StorableComponent):
    def __init__(self):
        self._root_dir = Directory('root')
        self._current_dir = self._root_dir

    def cd(self, file_path: str) -> None:
        if not _is_file_path_correct(file_path):
            raise PathNotExistsError(file_path)


class LocalStorage(StorableComponent):
    def __init__(self):
        self._root_dir = Directory('root')
        self._current_dir = self._root_dir
