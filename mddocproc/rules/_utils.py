import re

from typing import Tuple
from .._document import Document


def format_markdown_link(text: str, relative_path: str, section: str | None = None):
    """
    Creates a well formatted markdown link.
    :param text: The text to display as the markdown link.
    :param relative_path: The relative path to the file you want to link.
    :param section: If provided, this adds the subsection #... part so you can link to a subsection of another file.
    """
    section_part = f"#{section}" if section else ""
    return f"[{text}](<{relative_path}{section_part}>)"


def _replace_span(document: Document, start: int, end: int, replacement: str) -> str:
    """
    Replace a span of text in a document's contents - does not alter the document itself.
    :param document: The document contents to replace a span of.
    :param start: The start of the span.
    :param end: The end of the span.
    :param replacement: The string to replace the span with - does not need to be the same length.
    """
    return "".join([document.contents[:start], replacement, document.contents[end:]])


def _get_next_match(document: Document, pointer: int, regex: re.Pattern) -> Tuple[re.Match | None, int, int]:
    """
    Convenience function to "get the next match" of a regex, in the document, after the "pointer" which is just an
    index in the document contents string. Used to be able to go through a file bit by bit and process each match one at
    a time, while avoiding getting stuck on a match that isn't processed into something that doesn't match.
    """
    match = re.search(regex, document.contents[pointer:])
    """:type: re.Match"""
    if not match:
        return None, 0, 0
    start, end = match.span(0)[0] + pointer, match.span(0)[1] + pointer
    return match, start, end
