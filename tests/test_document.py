import unittest

from unittest.mock import patch
from pathlib import Path
from mddocformatter import loading, Document


class TestLoading(unittest.TestCase):
    def test_document_unchanged(self):
        doc = Document(Path(), "contents")
        self.assertEqual(doc.contents, doc._original_contents)
        self.assertTrue(doc.unchanged)
        self.assertEqual("", doc.changes())

    def test_document_changed(self):
        doc = Document(Path(), "contents")
        doc.contents = "changed"
        self.assertNotEqual(doc.contents, doc._original_contents)
        self.assertFalse(doc.unchanged)

    def test_document_changes_removed(self):
        doc = Document(
            Path(),
            "Line 1\n"
            "Line 2\n"
            "Line 3\n"
        )
        doc.contents = (
            "Line 1\n"
            "Line 3\n"
        )
        self.assertEqual("-Line 2\n", doc.changes(0))

    def test_document_changes_added(self):
        doc = Document(
            Path(),
            "Line 1\n"
            "Line 3\n"
        )
        doc.contents = (
            "Line 1\n"
            "Line 2\n"
            "Line 3\n"
        )
        self.assertEqual("+Line 2\n", doc.changes(0))

    def test_document_changes_modified(self):
        doc = Document(
            Path(),
            "Line 1\n"
            "Line 2\n"
            "Line 3\n"
        )
        doc.contents = (
            "Line 1\n"
            "Line 5\n"
            "Line 3\n"
        )
        self.assertEqual("-Line 2\n+Line 5\n", doc.changes(0))


if __name__ == "__main__":
    unittest.main()
