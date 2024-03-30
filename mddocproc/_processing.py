from ._consts import Passes, FunctionMacro
from ._document import Document, load_document
from typing import Dict
from pathlib import Path


class ProcessingSettings(object):
    def __init__(
        self,
        root_directory: Path = Path("./"),
        target_directory: Path = Path("./"),
        version_name: str = "",
        rule_set: list = None,
        macros: Dict[str, str | FunctionMacro] | None = None,
    ):
        """
        Settings to use when processing a document.
        :param root_directory: The root of the documentation tree.
        :param target_directory: The target_path directory under which to put the newly processed documents - can be
                                 the same as the root directory for in-place processing.
        :param version_name: The name of the version of the documentation, mostly used for confluence naming. Usually
                             develop or main.
        :param rule_set: The rules to run on each doc.
        :param macros: The macros to use for mass replacement throughout the docs. Can be None for no macros.
        """
        self.root_directory = root_directory
        self.target_directory = target_directory
        self.rules = rule_set or list()
        self.macros = macros or dict()
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

    def add_document(self, document: Document | Path):
        """
        Add a document to be processed.
        :document: The document to add.
        """
        if isinstance(document, Path):
            document = load_document(document)
            self.documents[document.input_path] = document
        elif isinstance(document, Document):
            self.documents[document.input_path] = document
        else:
            raise TypeError(f"Expected a Document or Path, got a {type(document).__name__}.")

    def run(self):
        for i in range(len(Passes)):
            for document in self.documents.values():
                for rules in filter(lambda x: x.pass_index == i, self.settings.rules):
                    rules(self, document)
        for document in self.documents.values():
            document.save()


def process_docs(
    input_dir: Path, output_dir: Path, rule_set: list, macros: Dict[str, FunctionMacro], version_name: str
):
    settings = ProcessingSettings(input_dir, output_dir, version_name, rule_set, macros)
    context = ProcessingContext(settings)
    for file_path in input_dir.glob("*.*"):
        context.add_document(file_path)
    context.run()
