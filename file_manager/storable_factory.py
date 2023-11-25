from file_manager.data_types.storable import (
    Directory,
    File,
    Document,
    StorableComponent,
)


class StorableFactory:
    def get_storable(
        self, storable_type: str, storable_name: str
    ) -> StorableComponent | None:
        if storable_type == "directory":
            return Directory(storable_name)
        elif storable_type == "file":
            return File(storable_name)
        elif storable_type == "document":
            return Document(storable_name)
        return None
