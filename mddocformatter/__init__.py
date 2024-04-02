import logging as _logging
from . import rules
from . import loading as loading
from .rules import DocumentRule, document_rule
from ._processing import ProcessingSettings, ProcessingContext, process_docs
from ._document import Document
from ._consts import DeploymentStyle, FunctionMacro


_logging.getLogger(__name__).addHandler(_logging.NullHandler())
