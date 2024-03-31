from __future__ import annotations

from ._base import document_rule

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .._processing import ProcessingContext
    from .._document import Document


@document_rule("*.md")
def add_glossary_links(context: ProcessingContext, document: Document):
    """
    Looks through a document for the first use of a word or phrase that is defined in the glossary. This can be either
    a top level entry or one of it's synonyms. This word / phrase in the document is then made into a link that
    references the glossary section where teh word / phrase is defined.
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    pass
