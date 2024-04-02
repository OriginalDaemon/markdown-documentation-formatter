from __future__ import annotations

from ._base import document_rule

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
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
    parts = list(document.input_path.parent.relative_to(context.settings.root_directory).parts)
    if context.settings.version_name:
        parts.insert(0, context.settings.version_name)
    parts = [" - ".join(parts[:i + 1]) for i in range(len(parts))]
    parent_dir = document.input_path.parents[0].parts[-1]
    if document.input_path.name.lower() == "readme.md" or document.input_path.name == f"{parent_dir}.md":
        filename = parts[-1] + ".md"
    else:
        filename = f"{parts[-1]} - {document.input_path.name}"
    document.target_path = context.settings.target_directory.joinpath(*parts) / filename
