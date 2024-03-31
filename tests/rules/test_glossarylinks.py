import unittest

from pathlib import Path
from mddocproc import ProcessingSettings, ProcessingContext, Document, rules


GLOSSARY_TEXT = """# Glossary
### Example
__*Synonyms: Demo, Demonstration*__
An example of a glossary term.

### Test Term
__*Synonyms: Example Term, Trial Word*__
An example of a multi-word term.
"""


class TestGlossaryLinks(unittest.TestCase):
    @staticmethod
    def _createContext(glossary_file_name="glossary.md"):
        settings = ProcessingSettings(root_directory=Path(__file__).parent / "data" / "docs")
        context = ProcessingContext(settings)
        context.add_document(Document(settings.root_directory / "glossary data" / glossary_file_name, GLOSSARY_TEXT))
        return context

    def test_link_term(self):
        context = self._createContext()
        doc = Document(Path(context.settings.root_directory / "test" / "test.md"), "Here is an Example of something.")
        rules.add_glossary_links(context, doc)
        self.assertEqual("Here is an [Example](<../glossary data/glossary.md#Example>) of something.", doc.contents)

    def test_link_synonym(self):
        context = self._createContext()
        doc = Document(Path(context.settings.root_directory / "test" / "test.md"), "Here is a demo of something.")
        rules.add_glossary_links(context, doc)
        self.assertEqual("Here is a [demo](<../glossary data/glossary.md#Example>) of something.", doc.contents)

    def test_link_term_preserve_case(self):
        context = self._createContext()
        doc = Document(Path(context.settings.root_directory / "test" / "test.md"), "Here is an eXaMpLe of something.")
        rules.add_glossary_links(context, doc)
        self.assertEqual("Here is an [eXaMpLe](<../glossary data/glossary.md#Example>) of something.", doc.contents)

    def test_link_phrase(self):
        context = self._createContext()
        doc = Document(Path(context.settings.root_directory / "test" / "test.md"), "Here is a Test Term.")
        rules.add_glossary_links(context, doc)
        self.assertEqual("Here is a [Test Term](<../glossary data/glossary.md#Test Term>).", doc.contents)

    def test_link_phrase_synonym(self):
        context = self._createContext()
        doc = Document(Path(context.settings.root_directory / "test" / "test.md"), "Here is an Example Term.")
        rules.add_glossary_links(context, doc)
        self.assertEqual("Here is an [Example Term](<../glossary data/glossary.md#Test Term>).", doc.contents)

    def test_link_term_and_phrase_with_conflict(self):
        context = self._createContext()
        doc = Document(
            Path(context.settings.root_directory / "test" / "test.md"), "Here is an Example Term as an Example."
        )
        rules.add_glossary_links(context, doc)
        self.assertEqual(
            "Here is an [Example Term](<../glossary data/glossary.md#Test Term>) as an "
            "[Example](<../glossary data/glossary.md#Example>).",
            doc.contents,
        )

    def test_skip_term_in_link_link_term(self):
        context = self._createContext()
        doc = Document(
            Path(context.settings.root_directory / "test" / "test.md"),
            "Here is an [Example](<www.google.com>) of something and another Example.",
        )
        rules.add_glossary_links(context, doc)
        self.assertEqual(
            "Here is an [Example](<www.google.com>) of something and another "
            "[Example](<../glossary data/glossary.md#Example>).",
            doc.contents,
        )

    def test_glossary_case_insensitive_glossary_filename(self):
        context = self._createContext("Glossary.md")
        doc = Document(Path(context.settings.root_directory / "test" / "test.md"), "Here is an Example of something.")
        rules.add_glossary_links(context, doc)
        self.assertEqual("Here is an [Example](<../glossary data/Glossary.md#Example>) of something.", doc.contents)


if __name__ == "__main__":
    unittest.main()
