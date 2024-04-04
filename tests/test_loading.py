import unittest

from unittest.mock import patch
from mddocformatter import loading, Document
from pathlib import Path

MACROS_TEXT = """author = "hello"
title = "world"


def capitalize(value):
    return value.capitalize()
"""


RULES_TEXT = """from mddocformatter import ProcessingContext, Document, document_rule


@document_rule("*.md")
def my_rule(context: ProcessingContext, document: Document):
    pass
"""


GLOSSARY_TEXT = """# Glossary
### Example
__*Synonyms: Demo, Demonstration*__
An example of a glossary term.

### Test Term
__*Synonyms: Example Term, Trial Word*__
An example of a multi-word term.
### Synonyms: something, something else
__*Synonyms: Example Term, Trial Word*__
An example of a definition that interferes with finding synonyms
"""


class TestLoading(unittest.TestCase):
    def test_load_doc_not_exist(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_is_dir:
                mock_exists.return_value = False
                mock_is_dir.return_value = False
                with self.assertRaises(FileNotFoundError):
                    loading.load_document(Path())

    def test_load_doc_isdir(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_is_dir:
                mock_exists.return_value = True
                mock_is_dir.return_value = True
                with self.assertRaises(IsADirectoryError):
                    loading.load_document(Path())

    def test_load_macros_from_module_contents(self):
        const_macros, function_macros = loading.load_macros_from_module_contents(MACROS_TEXT)
        self.assertIn("author", const_macros)
        self.assertEqual("hello", const_macros["author"])
        self.assertIn("title", const_macros)
        self.assertEqual("world", const_macros["title"])
        self.assertIn("capitalize", function_macros)
        self.assertTrue(callable(function_macros["capitalize"]))

    def test_macros_loading(self):
        with patch.object(loading, "load_document") as mock:
            mock.return_value = Document(Path("macros.py"), MACROS_TEXT)
            const_macros, function_macros = loading.load_macros_from_py_file(Path("macros.py"))
            self.assertIn("author", const_macros)
            self.assertEqual("hello", const_macros["author"])
            self.assertIn("title", const_macros)
            self.assertEqual("world", const_macros["title"])
            self.assertIn("capitalize", function_macros)
            self.assertTrue(callable(function_macros["capitalize"]))

    def test_load_custom_rules_from_module_contents(self):
        rule_set = loading.load_custom_rules_from_module_contents(RULES_TEXT)
        self.assertEqual(1, len(rule_set))
        self.assertTrue(any(x.__name__ == "my_rule" for x in rule_set))

    def test_rules_loading(self):
        with patch.object(loading, "load_document") as mock:
            mock.return_value = Document(Path("rules.py"), RULES_TEXT)
            rule_set = loading.load_custom_rules_from_py_file(Path("rules.py"))
            self.assertEqual(1, len(rule_set))
            self.assertTrue(any(x.__name__ == "my_rule" for x in rule_set))

    def test_process_glossary(self):
        glossary_data = loading.process_glossary(GLOSSARY_TEXT)
        expected = [
            ("synonyms: something, something else", "Synonyms: something, something else"),
            ("demonstration", "Example"),
            ("example term", "Test Term"),
            ("trial word", "Test Term"),
            ("test term", "Test Term"),
            ("example", "Example"),
            ("demo", "Example"),
        ]
        self.assertListEqual(expected, glossary_data)

    def test_glossary_loading(self):
        with patch.object(loading, "load_document") as mock:
            mock.return_value = Document(Path("glossary.md"), GLOSSARY_TEXT)
            glossary_data = loading.load_glossary(Path("glossary.md"))
            expected = [
                ("synonyms: something, something else", "Synonyms: something, something else"),
                ("demonstration", "Example"),
                ("example term", "Test Term"),
                ("trial word", "Test Term"),
                ("test term", "Test Term"),
                ("example", "Example"),
                ("demo", "Example"),
            ]
            self.assertListEqual(expected, glossary_data)

    def test_rules_not_py_file(self):
        with self.assertRaises(ValueError):
            loading.load_custom_rules_from_py_file(Path("something.md"))

    def test_macros_not_py_file(self):
        with self.assertRaises(ValueError):
            loading.load_macros_from_py_file(Path("something.md"))

    def test_glossary_not_md_file(self):
        with self.assertRaises(ValueError):
            loading.load_glossary(Path("something.py"))


if __name__ == "__main__":
    unittest.main()
