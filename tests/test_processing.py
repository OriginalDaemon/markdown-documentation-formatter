import unittest

from pathlib import Path
from unittest.mock import patch, MagicMock
from mddocformatter import ProcessingSettings, ProcessingContext, Document, rules, Passes, process_docs, validate_docs


class TestProcessing(unittest.TestCase):
    def test_context_add_document(self):
        root_dir = Path(__file__).parent / "data" / "docs"
        settings = ProcessingSettings(
            root_directory=root_dir,
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        context.add_document(Document(root_dir / "doc.md"))
        self.assertEqual(1, len(context.documents))

    def test_context_add_document_path(self):
        root_dir = Path(__file__).parent / "data" / "docs"
        settings = ProcessingSettings(
            root_directory=root_dir,
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        with patch("mddocformatter._processing.load_document") as mock:
            mock.return_value = Document(root_dir / "doc.md")
            context.add_document(root_dir / "doc.md")
            self.assertEqual(1, len(context.documents))

    def test_context_add_document_not_under_root(self):
        root_dir = Path(__file__).parent / "data" / "docs"
        settings = ProcessingSettings(
            root_directory=root_dir,
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        with self.assertRaises(ValueError):
            context.add_document(Document(Path("doc.md")))

    def test_context_get_document_by_name(self):
        root_dir = Path(__file__).parent / "data" / "docs"
        settings = ProcessingSettings(
            root_directory=root_dir,
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        context.add_document(Document(root_dir / "test" / "test - sub dir" / "test - sub dir - Doc.md"))
        cases = [
            "test - sub dir - Doc.md",  # fullname, case sensitive
            "test - sub dir - doc.md",  # fullname, case insensitive
            "test - sub dir - Doc",  # sans extension, case sensitive
            "test - sub dir - doc",  # sans extension, case insensitive
            "Doc.md",  # drop the confluence style prefix, fullname, case sensitive
            "doc.md",  # drop the confluence style prefix, fullname, case insensitive
            "Doc",  # drop the confluence style prefix, sans extension, case sensitive
            "doc",  # drop the confluence style prefix, sans extension, case insensitive
        ]
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                self.assertIsNotNone(context.get_document_by_name(case))

    def test_run(self):
        mock = MagicMock()
        rule = rules.DocumentRule(mock, "*.md", Passes.FINALIZE)
        root_dir = Path(__file__).parent / "data" / "docs"
        settings = ProcessingSettings(
            root_directory=root_dir, target_directory=Path(__file__).parent / "data" / "processed", rule_set=[rule]
        )
        context = ProcessingContext(settings)
        doc1, doc2 = Document(root_dir / "doc.md"), Document(root_dir / "image.png")
        context.add_document(doc1)
        context.add_document(doc2)
        context.run()
        self.assertEqual(2, len(context.documents))
        mock.assert_called_once()
        mock.assert_called_with(context, doc1)

    def test_context_save(self):
        root_dir = Path(__file__).parent / "data" / "docs"
        settings = ProcessingSettings(
            root_directory=root_dir,
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        context.add_document(Document(root_dir / "doc.md"))
        with patch("mddocformatter._processing.save_document") as mock:
            context.save()
            mock.assert_called_once()

    def test_process_docs(self):
        rule_func_mock = MagicMock()
        rule = rules.DocumentRule(rule_func_mock, "*.md", Passes.FINALIZE)
        root_dir = Path(__file__).parent / "data" / "docs"
        doc_path = root_dir / "doc.md"
        with patch.object(Path, "glob") as glob_mock:
            with patch("mddocformatter._processing.load_document") as load_document_mock:
                load_document_mock.return_value = Document(doc_path)
                glob_mock.return_value = [doc_path]
                result = process_docs(
                    input_dir=root_dir, output_dir=Path(__file__).parent / "data" / "processed", rule_set=[rule]
                )
                rule_func_mock.assert_called_once()
                self.assertTrue(result)

    def test_validate_docs(self):
        rule_func_mock = MagicMock()
        rule = rules.DocumentRule(rule_func_mock, "*.md", Passes.FINALIZE)
        root_dir = Path(__file__).parent / "data" / "docs"
        doc_path = root_dir / "doc.md"
        with patch.object(Path, "glob") as glob_mock:
            with patch("mddocformatter._processing.load_document") as load_document_mock:
                load_document_mock.return_value = Document(doc_path)
                glob_mock.return_value = [doc_path]
                result = validate_docs(input_dir=root_dir, rule_set=[rule])
                rule_func_mock.assert_called_once()
                self.assertTrue(result)

    def test_validate_docs_invalid(self):
        @rules.document_rule("*.md")
        def rule(c: ProcessingContext, d: Document):
            d.contents += "hello world"

        root_dir = Path(__file__).parent / "data" / "docs"
        doc_path = root_dir / "doc.md"
        with patch.object(Path, "glob") as glob_mock:
            with patch("mddocformatter._processing.load_document") as load_document_mock:
                load_document_mock.return_value = Document(doc_path)
                glob_mock.return_value = [doc_path]
                result = validate_docs(input_dir=root_dir, rule_set=[rule])
                self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
