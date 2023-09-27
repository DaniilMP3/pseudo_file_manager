class StorableCreationError(Exception):
    def __init__(self, name: str):
        super().__init__(f'Cannot create storable object {name}')


class PathNotExistsError(Exception):
    def __init__(self, file_path: str):
        super().__init__(f"Path: {file_path} doesn't exists")


class StorableNameNotAvailable(Exception):
    def __init__(self, storable_name: str):
        super().__init__(f"Storable name: {storable_name} is not available")


class StorableObjectAlreadyExists(Exception):
    def __init__(self, directory_name: str):
        super().__init__(f"Directory {directory_name} alreay exists")
