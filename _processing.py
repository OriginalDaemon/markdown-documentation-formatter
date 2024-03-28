from ._consts import PASSES
from ._document import Document, load_document
from typing import overload, Dict


class ProcessingSettings(object):
    def __init__(
        self, root_directory, target_directory, version_name: str, rules: list = None, consts: Dict[str, str] = None
    ):
        """
        Settings to use when processing a document.
        :param root_directory: The root of the documentation tree.
        :param target_directory: The target_path directory under which to put the newly processed documents - can be
                                 the same as the root directory for in-place processing.
        :param version_name: The name of the version of the documentation, mostly used for confluence naming. Usually
                             develop or main.
        :param rules: The rules to run on each doc.
        :param consts: The consts to use for mass replacement throughout the docs. Can be None for no consts.
        """
        self.root_directory = root_directory
        self.target_directory = target_directory
        self.rules = rules or list()
        self.consts = consts or dict()
        self.version_name = version_name


class ProcessingContext(object):
    def __init__(self, settings: ProcessingSettings):
        """
        A context under which all document processing jobs are ran. This owns the document data throughout out the
        document processing.
        :param settings: The settings used when processing the document.
        """
        self.settings = settings
        self.documents = {}

    @overload(str)
    def add_document(self, path: str):
        """
        Loads a document at a given file-path.
        :param path: the path to the document to add.
        """
        self.add_document(load_document(path))

    def add_document(self, document: Document):
        """
        Add a document to be processed.
        :document: The document to add.
        """
        self.documents[document.input_path] = document

    def run(self):
        for i in range(len(PASSES)):
            for document in self.documents.values():
                for rules in filter(lambda x: x.pass_index == i, self.settings.rules):
                    rules(self, document)
        for document in self.documents.values():
            document.save()
