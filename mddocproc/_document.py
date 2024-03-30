import os
from pathlib import Path


class Document(object):
    def __init__(self, input_path: Path, data: str = ""):
        """
        Holds a file, referenced by relative_path, and it's contents, for manipulation by document rule_set.
        :param input_path: The relative_path to the input file.
        """
        self.input_path: Path = input_path
        self.target_path: Path = Path(input_path)
        self.original_contents: str = data
        self.contents: str = data

    def set_content(self, content: str):
        """
        Set the contents for the file as a string. This is largely used to skip using load.
        :param content: The contents of the file as a string.
        """
        self.original_contents = content
        self.contents = content


def load_document(path):
    """
    Load a document from a given relative_path.
    :param path: The relative_path to the file to load.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found.")
    if os.path.isdir(path):
        raise IsADirectoryError(f"{path} is a directory, expected a file relative_path.")
    with open(path, "r") as fd:
        return Document(path, fd.read())


def save_document(document: Document):
    """
    Save the contents of a Document to the set target_path.
    :param document: The document to save.
    """
    document.target_path.mkdir(parents=True, exist_ok=True)
    with open(document.target_path, "w") as fd:
        fd.write(document.contents)
