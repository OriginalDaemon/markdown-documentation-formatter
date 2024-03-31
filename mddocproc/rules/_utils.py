import re
import os

from pathlib import Path
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


def format_document_markdown_link(
    text: str, source_document: Document, linked_document: Document, section: str | None = None
):
    """
    Creates a well formatted, relative markdown link from one document to a subsection of another.
    :param text: The text to display as the markdown link.
    :param source_document: The source document where you want to use the link.
    :param linked_document: The document you want to link to.
    :param section: If provided, this adds the subsection #... part so you can link to a subsection of another file.
    """
    return format_markdown_link(text, form_relative_link(source_document, linked_document), section)


def form_relative_link(source_document: Document, linked_document: Document) -> str:
    """
    Given a source document, and the document you want to link to, this forms a relative link string for use in a
    markdown link.
    :param source_document: The source document where you want to use the link.
    :param linked_document: The document you want to link to.
    :return: The relative link.
    """
    common = Path(os.path.commonpath([linked_document.input_path, source_document.input_path]))
    return os.path.join(
        os.path.relpath(common, source_document.input_path.parent), os.path.relpath(linked_document.target_path, common)
    ).replace("\\", "/")


def replace_span(document: Document, start: int, end: int, replacement: str) -> str:
    """
    Replace a span of text in a document's contents - does not alter the document itself.
    :param document: The document contents to replace a span of.
    :param start: The start of the span.
    :param end: The end of the span.
    :param replacement: The string to replace the span with - does not need to be the same length.
    """
    return "".join([document.contents[:start], replacement, document.contents[end:]])


def get_next_match(document: Document, pointer: int, regex: re.Pattern) -> Tuple[re.Match | None, int, int]:
    """
    Convenience function to "get the next match" of a regex, in the document, after the "pointer" which is just an
    index in the document contents string. Used to be able to go through a file bit by bit and process each match one at
    a time, while avoiding getting stuck on a match that isn't processed into something that doesn't match.
    """
    match: re.Match | None = re.search(regex, document.contents[pointer:])
    if not match:
        return None, 0, 0
    start, end = match.span(0)[0] + pointer, match.span(0)[1] + pointer
    return match, start, end
