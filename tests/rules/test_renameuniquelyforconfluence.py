import unittest

from pathlib import Path
from mddocproc import ProcessingSettings, ProcessingContext, Document, rules


class TestRenameUniquelyForConfluence(unittest.TestCase):
    def test_rename_readme(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "sub dir" / "readme.md", "")
        rules.rename_uniquely_for_confluence(context, doc)
        expected = Path(__file__).parent / "data" / "processed" / "sub dir" / "sub dir.md"
        self.assertEqual(expected, doc.target_path)

    def test_already_named_after_parent_dir(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "sub dir" / "sub dir.md", "")
        rules.rename_uniquely_for_confluence(context, doc)
        expected = Path(__file__).parent / "data" / "processed" / "sub dir" / "sub dir.md"
        self.assertEqual(expected, doc.target_path)

    def test_rename_readme_with_version(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed",
            version_name="beta",
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "sub dir" / "readme.md", "")
        rules.rename_uniquely_for_confluence(context, doc)
        expected = Path(__file__).parent / "data" / "processed" / "beta" / "sub dir" / "beta - sub dir.md"
        self.assertEqual(expected, doc.target_path)

    def test_rename_non_special_file(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "sub dir" / "general.md", "")
        rules.rename_uniquely_for_confluence(context, doc)
        expected = Path(__file__).parent / "data" / "processed" / "sub dir" / "sub dir - general.md"
        self.assertEqual(expected, doc.target_path)

    def test_rename_non_special_file_with_version(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed",
            version_name="beta",
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "sub dir" / "general.md", "")
        rules.rename_uniquely_for_confluence(context, doc)
        expected = Path(__file__).parent / "data" / "processed" / "beta" / "sub dir" / "beta - sub dir - general.md"
        self.assertEqual(expected, doc.target_path)


if __name__ == '__main__':
    unittest.main()
