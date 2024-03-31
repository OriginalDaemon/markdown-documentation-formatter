import unittest
from mddocproc import loading

MACROS_TEXT = """author = "hello"
title = "world"


def capitalize(value):
    return value.capitalize()
"""


RULES_TEXT = """from mddocproc import ProcessingContext, Document, document_rule


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
"""


class TestLoading(unittest.TestCase):
    def test_load_macros_from_module_contents(self):
        const_macros, function_macros = loading.load_macros_from_module_contents(MACROS_TEXT)
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

    def test_process_glossary(self):
        glossary_data = loading.process_glossary(GLOSSARY_TEXT)
        expected = [
            ("demonstration", "Example"),
            ("example term", "Test Term"),
            ("trial word", "Test Term"),
            ("test term", "Test Term"),
            ("example", "Example"),
            ("demo", "Example"),
        ]
        self.assertListEqual(expected, glossary_data)
