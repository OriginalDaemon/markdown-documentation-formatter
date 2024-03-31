import re

from enum import Enum
from typing import Callable, ParamSpec


class DeploymentStyle(Enum):
    """
    A set of standard "styles" which are used to configure common sets of rule_set.
    """

    GITHUB = "github"
    CONFLUENCE = "confluence"
    CUSTOM = "custom"


class Passes(Enum):
    """
    List of indices for the passes to run in the documentation processing step.
    """

    FIRST = 0
    LINK_UPDATING = 1
    FINALIZE = 2


P = ParamSpec("P")
FunctionMacro = Callable[P, str]


regex_const_macro = re.compile(r"\${([\w]+)}")
regex_function_macro = re.compile(r"\${([\w]+)\(([\w\s,]*)\)}")
regex_markdown_link = re.compile(r"\[([\w\s]+)\]\([<]*([\w\s\.-\\\/\-%]+[^>])[>]*\)")
regex_any_markdown_link = re.compile(r"\[[\w\s]+\]\([<]*[%\w\s\.-\\\/\-%]+[#%\w\s\.-\\\/\-]*[>]*\)")
regex_markdown_link_with_subsection = re.compile(r"\[([\w\s]+)\]\([<]*([\w\s\.-\\\/\-%]+[^>])#+(.*[^>])[>]*\)")
regex_glossary_synonyms = re.compile(r"synonyms\: ([\w\s,]+)", re.IGNORECASE)
