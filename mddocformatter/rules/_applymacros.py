from __future__ import annotations

import logging
import inspect

from ._base import document_rule
from ._utils import get_next_match, replace_span
from .._consts import regex_const_macro, regex_function_macro

from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .._processing import ProcessingContext
    from .._document import Document


logger = logging.getLogger(__name__)


def _replace_const_macros(context: ProcessingContext, document: Document):
    pointer = 0
    while pointer < len(document.contents):
        match, start, end = get_next_match(document, pointer, regex_const_macro)
        if not match:
            break
        macroName = match.group(1)
        macro = context.settings.const_macros.get(macroName, None)
        if macro is not None:
            document.contents, _ = replace_span(document, start, end, context.settings.const_macros[macroName])
            pointer = start
        elif macro is None and context.settings.function_macros.get(macroName, None) is not None:
            logger.exception(
                f"Exception encountered trying to resolve {match.group(0)} as {macroName} is a function, not a const."
            )
            pointer = end
        else:
            logger.warning(
                f"Invalid macro: found {match.group(0)} in {document.input_path}, but no matching macro is defined."
            )
            pointer = end


def _extract_args(value: str) -> Tuple[str, ...]:
    return tuple(map(lambda x: x.strip(), value.split(","))) if value else ()


def _run_function_macro(
    context: ProcessingContext, functionName: str, args: Tuple[str, ...], origin_match: str
) -> str | None:
    # noinspection PyBroadException
    try:
        return context.settings.function_macros[functionName](*args)
    except Exception:
        signature = inspect.signature(context.settings.function_macros[functionName])
        if len(args) != len(signature.parameters):
            logger.exception(
                f"Exception encountered trying to resolve {origin_match} using {signature}. "
                f"Expected {len(signature.parameters)} args, got {len(args)}."
            )
        else:
            logger.exception(f"Exception encountered trying to resolve {origin_match} using {signature}.")
    return None


def _replace_function_macros(context: ProcessingContext, document: Document):
    pointer = 0
    while pointer < len(document.contents):
        match, start, end = get_next_match(document, pointer, regex_function_macro)
        if not match:
            break
        macroName = match.group(1)
        success = False
        if macroName in context.settings.function_macros:
            args = _extract_args(match.group(2))
            value = _run_function_macro(context, macroName, args, match.group(0))
            if value is not None:
                document.contents, end = replace_span(document, start, end, value)
                success = True
        elif macroName in context.settings.const_macros:
            logger.exception(
                f"Exception encountered trying to resolve {match.group(0)} as {macroName} is not a function."
            )
        else:
            logger.warning(
                f"Invalid macro: found {match.group(0)} in {document.input_path}, but no matching macro is defined."
            )
        if success:
            pointer = start
        else:
            pointer = end


@document_rule("*.md")
def apply_macros(context: ProcessingContext, document: Document):
    """
    Applies any defined macros to the document.
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    _replace_const_macros(context, document)
    _replace_function_macros(context, document)
