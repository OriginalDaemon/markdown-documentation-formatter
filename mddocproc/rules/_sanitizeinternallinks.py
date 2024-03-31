from __future__ import annotations

import re
import os

from pathlib import Path
from urllib.parse import unquote
from ._base import document_rule
from ._utils import _get_next_match, _replace_span
from .._consts import regex_markdown_link, regex_markdown_link_with_subsection

from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .._processing import ProcessingContext
    from .._document import Document


def _get_document_from_link(context: ProcessingContext, document: Document, link: str) -> Document | None:
    result = context.get_document((document.input_path.parent / link).resolve())
    if not result:
        result = context.get_document((context.settings.root_directory / link).resolve())
    return result


def _get_next_link_match(document: Document, pointer: int) -> Tuple[bool, int, int, str, str, str]:
    match, start, end = _get_next_match(document, pointer, regex_markdown_link_with_subsection)
    if match:
        return True, start, end, match.group(1), match.group(2), match.group(3)
    else:
        match, start, end = _get_next_match(document, pointer, regex_markdown_link)
        if match:
            return True, start, end, match.group(1), match.group(2), ""
        else:
            return False, 0, 0, "", "", ""


def _form_relative_link(source_document: Document, linked_document: Document) -> str:
    common = Path(os.path.commonpath([linked_document.input_path, source_document.input_path]))
    return os.path.join(
        os.path.relpath(common, source_document.input_path.parent), os.path.relpath(linked_document.target_path, common)
    ).replace("\\", "/")


def _process_section_reference(section: str, linked_document: Document):
    if section:
        # find the actual linked section and recreate teh section reference.
        regex_section_part = unquote(section).replace("-", "[ -]")
        section_regex = re.compile(r"#+\s*(" + regex_section_part + ")")
        for line in linked_document.contents.split("\n"):
            result = re.search(section_regex, line)
            if result:
                section = result.group(1)
                break
    return section


@document_rule("*.md")
def santize_internal_links(context: ProcessingContext, document: Document):
    """
    Find any "internal" markdown links and make sure they use the form ()[<relative_path to item>]
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    from ._utils import format_markdown_link

    pointer = 0
    while pointer < len(document.contents):
        success, start, pointer, text, path, section = _get_next_link_match(document, pointer)
        linked_document = _get_document_from_link(context, document, unquote(path))
        if linked_document is not None:
            path = _form_relative_link(document, linked_document)
            section = _process_section_reference(section, linked_document)
            reformatted_link = format_markdown_link(text, path, section)
            document.contents = _replace_span(document, start, pointer, reformatted_link)
