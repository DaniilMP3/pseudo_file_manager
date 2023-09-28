import unittest
from googledrive_cli.exceptions import (
    StorableNameNotAvailable,
    StorableNameAlreadyExists,
    StorableObjectNotExists,
)
from googledrive_cli.data_types.storable import Directory, Document


class TestCompositePattern(unittest.TestCase):
    def test_directory_creation(self):
        with self.assertRaises(StorableNameNotAvailable):
            Directory("")

        with self.assertRaises(StorableNameNotAvailable):
            Directory("directory with whitespaces")

        with self.assertRaises(StorableNameNotAvailable):
            Directory("directory/with/!@specific!!![symbols")

        directory1 = Directory("directory_with_underscore")
        self.assertEquals(directory1.get_name(), "directory_with_underscore")

        directory2 = Directory("StandardDirectory")
        self.assertEquals(directory2.get_name(), "StandardDirectory")

        directory3 = Directory("directory.with.dots")
        self.assertEquals(directory3.get_name(), "directory.with.dots")

    def test_add_storable_to_folder(self):
        directory1 = Directory("Directory")
        with self.assertRaises(StorableNameNotAvailable):
            directory1.add(Document("unavailable storable name @!!#"))
        with self.assertRaises(StorableNameNotAvailable):
            directory1.add(Directory("unavailable directory.name "))

        new_document = Document("Document", document_text="test text")
        directory1.add(new_document)
        self.assertEquals(True, new_document in directory1.storable_objects)

    def test_add_existing_component_to_directory(self):
        directory1 = Directory("Directory")

        document = Document("Document")
        directory1.add(document)

        with self.assertRaises(StorableNameAlreadyExists):
            directory1.add(document)

    def get_child_from_directory(self):
        directory = Directory("Directory")

        document1 = Document("Doc1")
        document2 = Document("Doc2")

        directory.add(document1)
        directory.add(document2)

        retrieved = directory.get_child("Doc2")
        self.assertEquals(retrieved, document2)

        with self.assertRaises(StorableObjectNotExists):
            directory.get_child("NotExistentDocument")


if __name__ == "__main__":
    unittest.main()
