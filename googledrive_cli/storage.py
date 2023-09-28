from googledrive_cli.data_types.storable import Directory, StorableComponent
from googledrive_cli.exceptions import PathNotExistsError
from typing import Type


def __pre_process_path(path: str) -> str:
    path.strip("/")
    flag = False
    for i, char in enumerate(path):
        if char in "\\":  # Unavailable separator
            return ""
        if char == "/" and flag:
            path = path[:i] + path[i + 1 :]  # Remove extra '/'
        elif char == "/" and not flag:
            flag = True
    return path


def pre_process_path(func):
    def wrapper(self, path):
        path = __pre_process_path(path)
        return func(self, path)

    return wrapper


class Storage(StorableComponent):
    def __init__(self):
        self._root_dir = Directory("root")
        self.current_dir = self._root_dir

    def _find_component(
        self, path: str, find_from_root: bool = False
    ) -> Type[StorableComponent]:
        """
        Find component in file system 'tree'
        """
        current_directory = self.current_dir
        if find_from_root:
            current_directory = self._root_dir

        path_components = path.split("/")

        for i, component in enumerate(path_components):
            component_found = False
            for storable in current_directory.storable_objects:
                if isinstance(storable, Directory) and storable.get_name() == component:
                    current_directory = storable
                    component_found = True
                    break

            if not component_found and i == len(path_components) - 1:
                for storable in current_directory.storable_objects:
                    if storable.get_name() == component:
                        return storable

            if not component_found:
                raise PathNotExistsError(path)

        return current_directory

    @pre_process_path
    def cd(self, path: str) -> None:
        if not path:
            self.current_dir = self._root_dir
            return

        founded_directory = self._find_component(path)
        if not isinstance(founded_directory, Directory):
            raise PathNotExistsError(path)

        self.current_dir = founded_directory

    def add(self, new_component: Type[StorableComponent]) -> None:
        self.current_dir.add(new_component)

    def display(self):
        self.current_dir.display()


class CloudStorage(Storage):
    def __init__(self):
        super().__init__()

    @pre_process_path
    def download_component(self, path: str) -> Type[StorableComponent]:
        founded_component = self._find_component(path, True)
        return founded_component


class LocalStorage(Storage):
    def __init__(self):
        super().__init__()
