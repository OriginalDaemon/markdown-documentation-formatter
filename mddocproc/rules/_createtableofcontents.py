from __future__ import annotations

from ._base import document_rule

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .._processing import ProcessingContext
    from .._document import Document


def _calculate_toc_indent_for_heading(line) -> int:
    """:return: the indent to use for a heading link in a toc based on the heading size."""
    return (max(0, len(line) - len(line.lstrip("#")) - 1)) * 2


def _create_toc_from_sections(lines):
    from ._utils import format_markdown_link

    table_entries = []
    for line in map(lambda x: x.strip(), lines):
        if line.startswith("#"):
            indent_size = _calculate_toc_indent_for_heading(line)
            stripped = line.lstrip("#").strip()
            table_entries.append((indent_size, " - {}".format(format_markdown_link(stripped, "", stripped))))

    # Use smallest_indent to shift entire toc leftwards as much as we can...
    smallest_indent = min(x[0] for x in table_entries) if table_entries else 0
    toc = "\n".join(["{}{}".format(" " * (x[0] - smallest_indent), x[1]) for x in table_entries])

    return toc


@document_rule("*.md")
def create_table_of_contents(context: ProcessingContext, document: Document):
    """
    Create a table of contents wherever the document has the variable ${create_table_of_contents}
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    TABLE_OF_CONTENTS_VARIABLE = "${create_table_of_contents}"
    lines = document.contents.split("\n")
    processed = []
    for i, line in enumerate(lines):
        if TABLE_OF_CONTENTS_VARIABLE in line:
            table = _create_toc_from_sections(lines[i + 1 :])
            line = line.replace(TABLE_OF_CONTENTS_VARIABLE, table)
        processed.append(line)
    document.contents = "\n".join(processed)
