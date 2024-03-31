import unittest
from mddocproc import loading


GLOSSARY_TEXT = """# Glossary
### Example
__*Synonyms: Demo, Demonstration*__
An example of a glossary term.

### Test Term
__*Synonyms: Example Term, Trial Word*__
An example of a multi-word term.
"""


class TestLoading(unittest.TestCase):
    def test_process_glossary(self):
        loading.process_glossary(GLOSSARY_TEXT)
