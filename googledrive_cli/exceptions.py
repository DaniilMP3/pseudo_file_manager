class StorableCreationError(Exception):
    def __init__(self, name: str):
        super().__init__(f'Cannot create storable object {name}')


class PathNotExistsError(Exception):
    def __init__(self, file_path: str):
        super().__init__(f"Path: {file_path} doesn't exists")


class StorableNameNotAvailable(Exception):
    def __init__(self, storable_name: str):
        super().__init__(f"Storable name: {storable_name} is not available")


class StorableNameAlreadyExists(Exception):
    def __init__(self, storable_name: str):
        super().__init__(f"Storable object with name: {storable_name} already exists")


class StorableObjectNotExists(Exception):
    def __init__(self, storable_name: str):
        super().__init__(f"Cannot find {storable_name} storable object")
