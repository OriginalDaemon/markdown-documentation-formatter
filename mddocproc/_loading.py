import importlib
import importlib.util

from pathlib import Path
from typing import Dict, List, Tuple
from ._rules import DocumentRule
from ._consts import FunctionMacro


def load_macros_from_py_file(python_file_path: Path) -> Tuple[Dict[str, str], Dict[str, FunctionMacro]]:
    """
    Import a python file and load any macros defined within it. Consts are expected to be simple strings, and any
    functions are expected to return a string.
    Private macros, a.k.a. those with a name starting _, will be skipped.
    :param python_file_path: The relative_path to the python file where the macros are defined.
    :return: Dictionary of const names and their values and a dictionary of function macros.
    """
    const_macros: Dict[str, str] = {}
    function_macros: Dict[str, FunctionMacro] = {}
    if not python_file_path.exists() or not python_file_path.is_file():
        return const_macros, function_macros

    spec = importlib.util.spec_from_file_location("macros", str(python_file_path.resolve()))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for each in dir(module):
            if not each.startswith("_"):
                value = getattr(module, each)
                if callable(value):
                    function_macros[each] = value
                else:
                    const_macros[each] = value
    return const_macros, function_macros


def load_custom_rules_from_py_file(python_file_path: Path) -> List[DocumentRule]:
    """
    Loads a list of DocumentRules from a given python module. Rules are skipped if they are private; a.k.a. the rule
    name starts with _.
    :param python_file_path: The relative_path to the python module where rules are defined.
    """
    rules: List[DocumentRule] = []
    if not python_file_path.exists() or not python_file_path.is_file():
        return rules

    spec = importlib.util.spec_from_file_location("macros", str(python_file_path.resolve()))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for each in dir(module):
            value = getattr(module, each)
            if not each.startswith("_") and isinstance(value, DocumentRule):
                rules.append(value)
    return rules
