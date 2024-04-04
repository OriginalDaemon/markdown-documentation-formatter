import re

from pathlib import Path
from typing import Dict, List, Tuple
from types import ModuleType
from .rules import DocumentRule
from ._document import Document
from ._consts import FunctionMacro, regex_glossary_synonyms


def load_document(path: Path):
    """
    Load a document from a given path.
    :param path: The path to the file to load.
    """
    if not path.exists():
        raise FileNotFoundError(f"{path} not found.")
    if path.is_dir():
        raise IsADirectoryError(f"{path} is a directory, expected a file relative_path.")
    with open(path, "r") as fd:
        return Document(path, fd.read())


def save_document(document: Document):  # pragma: no cover
    """
    Save the contents of a Document to the set target_path.
    :param document: The document to save.
    """
    document.target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(document.target_path, "w+") as fd:
        fd.write(document.contents)


def _import_module(module_name: str, module_contents) -> ModuleType:
    module = ModuleType(module_name)
    exec(module_contents, module.__dict__)
    return module


def _process_consts_module(module: ModuleType) -> Tuple[Dict[str, str], Dict[str, FunctionMacro]]:
    const_macros: Dict[str, str] = {}
    function_macros: Dict[str, FunctionMacro] = {}
    for each in dir(module):
        if not each.startswith("_"):
            value = getattr(module, each)
            if callable(value):
                function_macros[each] = value
            else:
                const_macros[each] = value
    return const_macros, function_macros


def load_macros_from_module_contents(module_contents: str) -> Tuple[Dict[str, str], Dict[str, FunctionMacro]]:
    """
    Parse a python module from a string and load any macros defined within it. Consts are expected to be simple strings,
    and any functions are expected to take 0 or more strings as arguments and return a string.
    Private macros, a.k.a. those with a name starting _, will be skipped.
    :param module_contents: A string which constitutes the contents of the module. Usually obtained by reading a python
                            module as text.
    :return: Dictionary of const names and their values and a dictionary of function macros.
    """
    return _process_consts_module(_import_module("__macros_module", module_contents))


def load_macros_from_py_file(python_file_path: Path) -> Tuple[Dict[str, str], Dict[str, FunctionMacro]]:
    """
    Load a python module from a given file path and return the macros defined within.
    See: load_macros_from_module_contents for more details.
    :param python_file_path: The relative_path to the python file where the macros are defined.
    :return: Dictionary of const names and their values and a dictionary of function macros.
    """
    if python_file_path.suffix != ".py":
        raise ValueError(f"The file given is expected to be a python module file: {python_file_path}")
    return load_macros_from_module_contents(load_document(python_file_path).contents)


def _process_custom_rules_module(module: ModuleType) -> List[DocumentRule]:
    rules = []
    for each in dir(module):
        value = getattr(module, each)
        if not each.startswith("_") and isinstance(value, DocumentRule):
            rules.append(value)
    return rules


def load_custom_rules_from_module_contents(module_contents: str) -> List[DocumentRule]:
    """
    Extracts a list of DocumentRules from a given python module. Rules are skipped if they are private; a.k.a. the rule
    name starts with _.
    :param module_contents: A string which constitutes the contents of the module. Usually obtained by reading a python
                            module as text.
    :return: A list of DocumentRules defined in the given module contents.
    """
    return _process_custom_rules_module(_import_module("__custom_rules_module", module_contents))


def load_custom_rules_from_py_file(python_file_path: Path) -> List[DocumentRule]:
    """
    Load a python module from a given file path and return the DocumentRules defined within.
    See: load_custom_rules_module for more details.
    :param python_file_path: The relative_path to the python module where rules are defined.
    """
    if python_file_path.suffix != ".py":
        raise ValueError(f"The file given is expected to be a python module file: {python_file_path}")
    return load_custom_rules_from_module_contents(load_document(python_file_path).contents)


def process_glossary(glossary: str) -> List[Tuple[str, str]]:
    """
    Processes glossary data, loaded from a file, and returns a list of terms for later use. List is sorted from
    longest to shortest term.
    The list is a tuple of: term/phrase, term subsection
    e.g. [(a term, #A Term), (synonym of a term, #A Term), ...]
    """
    def extend_glossary_data(_glossary_data, _term, _section):
        if _term.lower() not in [x[0] for x in _glossary_data]:
            _glossary_data.append((_term.lower(), _section))

    glossary_data: List[Tuple[str, str]] = []
    lines = glossary.split("\n")
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("##"):
            term = line[len(line) - len(line.lstrip("#")) :].strip()
            section = term
            extend_glossary_data(glossary_data, term, section)
            for i in range(i + 1, len(lines)):
                line = lines[i].strip()
                match = re.search(regex_glossary_synonyms, line.lower())
                if match:
                    for synonym in list(map(lambda x: x.strip(), match.group(1).split(","))):
                        extend_glossary_data(glossary_data, synonym, section)
                    break

    glossary_data.sort(key=lambda x: len(x[0]), reverse=True)
    return glossary_data


def load_glossary(glossary_file_path: Path) -> List[Tuple[str, str]]:
    """
    Loads the glossary markdown file and creates a table of terms for later use. The list is sorted from longest to
    shortest phrase.
    See: Process glossary for more details.
    """
    if glossary_file_path.suffix != ".md":
        raise ValueError(f"The glossary file is expected to be a markdown file: {glossary_file_path}")
    return process_glossary(load_document(glossary_file_path).contents)
