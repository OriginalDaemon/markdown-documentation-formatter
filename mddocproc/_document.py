import os

from ._utils import make_directory


class Document(object):
    def __init__(self, input_path: str, data: str = ""):
        """
        Holds a file, referenced by path, and it's contents, for manipulation by document rule_set.
        :param input_path: The path to the input file.
        """
        self.input_path = input_path
        self.target_path = input_path
        self.original_contents = data
        self.contents = data

    @property
    def parent_dir_name(self) -> str:
        """
        :return: The name of the directory in which the document lives.
        """
        return os.path.dirname(self.input_path).split(os.path.sep)[-1]

    def set_content(self, content: str):
        """
        Set the contents for the file as a string. This is largely used to skip using load.
        :param content: The contents of the file as a string.
        """
        self.original_contents = content
        self.contents = content


def load_document(path):
    """
    Load a document from a given path.
    :param path: The path to the file to load.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found.")
    if os.path.isdir(path):
        raise IsADirectoryError(f"{path} is a directory, expected a file path.")
    with open(path, "r") as fd:
        return Document(path, fd.read())


def save_document(document: Document):
    """
    Save the contents of a Document to the set target_path.
    :param document: The document to save.
    """
    make_directory(os.path.dirname(document.target_path))
    with open(document.target_path, "w") as fd:
        fd.write(document.contents)
