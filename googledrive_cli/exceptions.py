class StorableCreationError(Exception):
    def __init__(self, name: str):
        super().__init__(f'Cannot create storable object {name}')