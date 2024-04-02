import unittest

from pathlib import Path
from mddocformatter import ProcessingSettings, ProcessingContext, Document, rules


class TestTableOfContents(unittest.TestCase):
    def test_empty_toc(self):
        context = ProcessingContext(ProcessingSettings())
        input_md = "# Title\n" "## Table of contents\n" "${create_table_of_contents}\n" "...\n" "...\n" "...\n"
        expected = "# Title\n" "## Table of contents\n" "\n" "...\n" "...\n" "...\n"
        doc = Document(Path("test.md"), input_md)
        rules.create_table_of_contents(context, doc)
        self.assertEqual(expected, doc.contents)

    def test_full_toc(self):
        context = ProcessingContext(ProcessingSettings())
        input_md = (
            "# Title\n"
            "## Table of contents\n"
            "${create_table_of_contents}\n"
            "## Section 1\n"
            "...\n"
            "### Subsection 1.1\n"
            "...\n"
            "### Subsection 1.2\n"
            "...\n"
            "## Section 2\n"
            "...\n"
            "### Subsection 2.1\n"
            "...\n"
        )
        expected = (
            "# Title\n"
            "## Table of contents\n"
            " - [Section 1](<#Section 1>)\n"
            "   - [Subsection 1.1](<#Subsection 1.1>)\n"
            "   - [Subsection 1.2](<#Subsection 1.2>)\n"
            " - [Section 2](<#Section 2>)\n"
            "   - [Subsection 2.1](<#Subsection 2.1>)\n"
            "## Section 1\n"
            "...\n"
            "### Subsection 1.1\n"
            "...\n"
            "### Subsection 1.2\n"
            "...\n"
            "## Section 2\n"
            "...\n"
            "### Subsection 2.1\n"
            "...\n"
        )
        doc = Document(Path("test.md"), input_md)
        rules.create_table_of_contents(context, doc)
        self.assertEqual(expected, doc.contents)


if __name__ == "__main__":
    unittest.main()
