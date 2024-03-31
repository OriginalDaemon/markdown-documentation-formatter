from __future__ import annotations

import os

from ._base import document_rule

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .._processing import ProcessingContext
    from .._document import Document


@document_rule()
def move_to_target_dir_relative(context: ProcessingContext, document: Document):
    """
    Move the target_path file to save a document to, to the same place under the target_path directory.
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    if context.settings.target_directory and context.settings.root_directory != context.settings.target_directory:
        rel_path = os.path.relpath(context.settings.root_directory, document.input_path)
        document.target_path = context.settings.target_directory / rel_path
