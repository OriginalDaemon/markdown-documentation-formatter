from __future__ import annotations

import functools

from fnmatch import fnmatch
from .._consts import Passes

from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from .._processing import ProcessingContext
    from .._document import Document


class DocumentRule(object):
    def __init__(
        self,
        function: Callable[[ProcessingContext, Document], None],
        file_filter: str,
        pass_index: Passes = Passes.FIRST,
    ):
        """
        Function decorator to create a document processor function. These functions will be called by a
        ProcessingContext to apply augmentations to a file that is loaded in memory.
        :param function: The function being decorated as a document processor.
        :param file_filter: fnmatch style file filter.
        :param pass_index: The index of the "pass" of the documents in which to operate. Sometimes rule_set need to wait
                           for other rule_set to run first.
        """
        self.function = function
        self.file_filter = file_filter
        self.pass_index = pass_index
        functools.update_wrapper(self, self.function)

    def _applies(self, document: Document):
        return fnmatch(str(document.input_path.resolve()), self.file_filter)

    def __call__(self, context: ProcessingContext, document: Document):
        if self._applies(document):
            self.function(context, document)


def document_rule(
    file_filter: str = "*.*", pass_index: Passes = Passes.FIRST
) -> Callable[[Callable[[ProcessingContext, Document], None]], DocumentRule]:
    """
    A wrapper to make simple DocumentRules from functions.
    :param file_filter: fnmatch style file filter string.
    :param pass_index: The index of the "pass" of the documents in which to operate. Sometimes rule_set need to wait for
                       other rule_set to run first.
    :return: A document rule type.
    """

    def _inner(func):
        return DocumentRule(func, file_filter, pass_index)

    return _inner
