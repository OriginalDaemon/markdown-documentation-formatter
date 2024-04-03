from __future__ import annotations

import re
import logging

from .._consts import regex_markdown_link
from ._base import document_rule
from ._utils import form_relative_link, replace_span, format_markdown_link

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .._processing import ProcessingContext
    from .._document import Document


logger = logging.getLogger(__name__)


def _is_inside_markdown_link(index: int, pointer: int, document: Document) -> int:
    """
    Work out if a given char index is inside of a markdown link.
    :param index: The index of the string you're looking at.
    :param pointer: The current index of the document we're searching from.
    :param document: The document to find markdown links within.
    :return: The index of the end of the markdown link you're within, if you're within one. -1 otherwise.
    """
    for match in re.finditer(regex_markdown_link, document.contents[pointer:]):
        start, end = match.span(0)[0] + pointer, match.span(0)[1] + pointer
        if start < index < end:
            return end
        elif index < start:
            break
    return -1


def has_glossary_link(term: str, section: str, link: str, document: Document) -> bool:
    """:return: True if the document already has a link for a given glossary term (case-insensitive)."""
    markdown_link = format_markdown_link(term, link, section)
    return markdown_link.lower() in document.contents.lower()


@document_rule("*.md")
def add_glossary_links(context: ProcessingContext, document: Document):
    """
    Looks through a document for the first use of a word or phrase that is defined in the glossary. This can be either
    a top level entry or one of it's synonyms. This word / phrase in the document is then made into a link that
    references the glossary section where teh word / phrase is defined.
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    from .. import loading

    glossary = context.get_document_by_name("glossary.md")
    if not glossary:
        logger.warning("Cannot find a glossary.md file, therefore skipping add_glossary_links.")
    elif glossary is not document:  # we don't want to modify the glossary to link to itself.
        glossary_data = loading.process_glossary(glossary.original_contents)
        link = form_relative_link(document, glossary)
        for term, section in glossary_data:
            if not has_glossary_link(term, section, link, document):
                pointer = 0
                while pointer < len(document.contents):
                    match_index = document.contents[pointer:].lower().find(term)
                    if match_index >= 0:
                        match_index += pointer
                        link_index = _is_inside_markdown_link(match_index, pointer, document)
                        if link_index >= 0:
                            pointer = link_index
                        else:
                            start, end = match_index, match_index + len(term)
                            markdown_link = format_markdown_link(document.contents[start:end], link, section)
                            document.contents = replace_span(document, start, end, markdown_link)
                            break
                    else:
                        break
