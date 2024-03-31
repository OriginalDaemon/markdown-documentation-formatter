from __future__ import annotations

import os

from ._base import document_rule

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .._processing import ProcessingContext
    from .._document import Document


@document_rule("*.md")
def rename_uniquely_for_confluence(context: ProcessingContext, document: Document):
    """
    Renames each page so that it contains its own tree as part of its name for the purpose of making the file
    uniquely named. This is to comply with the need in confluence for all pages to have unique names. This also
    renames "README.md" files after their parent directory.

    This will also place the version_name as the root directory.
    So, given a page:
      - "something/else/aswell.md
    this rule will rename it to
      - "develop/something/else/something - else - aswell.md
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    rel_path = os.path.relpath(context.settings.root_directory, document.input_path)
    rel_path = rel_path.replace(".md", "")  # remove file extension, we know it's .md
    parts = [context.settings.version_name] + rel_path.split(os.path.sep)
    parent_dir = os.path.dirname(os.path.dirname(rel_path))
    basename = os.path.basename(document.input_path)
    if basename.lower() == "readme.md" or basename == f"{parent_dir}.md":
        parts = parts[:-1] + [" - ".join(parts[:-1]) + ".md"]
    else:
        parts = parts[:-1] + [" - ".join(parts) + ".md"]
    document.target_path = context.settings.target_directory.joinpath(*parts)
