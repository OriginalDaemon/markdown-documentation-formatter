import logging as _logging
from . import _rules as rules
from ._rules import DocumentRule, document_rule
from ._processing import ProcessingSettings, ProcessingContext, process_docs
from ._document import Document
from ._consts import DeploymentStyle, FunctionMacro
from ._loading import load_macros_from_py_file, load_custom_rules_from_py_file


_logging.getLogger(__name__).addHandler(_logging.NullHandler())
