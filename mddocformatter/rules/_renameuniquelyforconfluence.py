from __future__ import annotations

import re

from ._base import document_rule
from pathlib import Path
from ._movetotargetdirrelative import move_to_target_dir_relative

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .._processing import ProcessingContext
    from .._document import Document


def path_is_confluence_style(root_directory: Path, input_path: Path, version_name: str) -> bool:
    """
    Test a path to see if it already conforms to the "confluence unique" form.
    The confluence unique form is where all file names and directories include the name of all parent directores,
    separated by " - ", up to the documentation root. This ensures they are unique in confluence if used in a space
    only containing documentation processed with this system.
    :param root_directory: The root directory for the documentation.
    :param input_path: The path to test.
    :param version_name: the version name from the settings.
    :return: True if the path is already a valid "confluence style" path.
    """
    rel_path = input_path.relative_to(root_directory)
    for i, part in enumerate(rel_path.parts):
        if version_name and version_name not in part:
            return False
        if i > 0 and (i < len(rel_path.parts) - 1) and not re.match(f"{rel_path.parts[i - 1]} - .+", part):
            return False

    if len(rel_path.parts) > 1:
        return (
            input_path.name == f"{rel_path.parts[-2]}.md" or
            re.match(f"{rel_path.parts[-2]} - .+.md", input_path.name) is not None
        )
    else:
        return not version_name or re.match(f"{version_name} - .+.md", input_path.name) is not None


@document_rule("*.md")
def rename_uniquely_for_confluence(context: ProcessingContext, document: Document):
    """
    Renames each page so that it contains its own tree as part of its name for the purpose of making the file
    uniquely named. This is to comply with the need in confluence for all pages to have unique names. This also
    renames "README.md" files after their parent directory.

    This will also place the version_name as the root directory.
    So, given a page:
      - "something/else/as well.md
    this rule will rename it to
      - "develop/something/else/something - else - as well.md
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    if path_is_confluence_style(context.settings.root_directory, document.input_path, context.settings.version_name):
        move_to_target_dir_relative(context, document)
    else:
        parts = list(document.input_path.parent.relative_to(context.settings.root_directory).parts)
        if context.settings.version_name:
            parts.insert(0, context.settings.version_name)
        parts = [" - ".join(parts[: i + 1]) for i in range(len(parts))]
        parent_dir = document.input_path.parents[0].parts[-1]
        if not parts:
            filename = document.input_path.name
        elif document.input_path.name.lower() == "readme.md" or document.input_path.name == f"{parent_dir}.md":
            filename = parts[-1] + ".md"
        else:
            filename = f"{parts[-1]} - {document.input_path.name}"
        document.target_path = context.settings.target_directory.joinpath(*parts) / filename
