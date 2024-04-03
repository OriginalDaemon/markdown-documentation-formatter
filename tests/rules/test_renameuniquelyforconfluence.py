import unittest

from pathlib import Path
from mddocformatter import ProcessingSettings, ProcessingContext, Document, rules


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
        expected = Path(__file__).parent / "data" / "processed" / "beta" / "beta - sub dir" / "beta - sub dir.md"
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
        expected = (
            Path(__file__).parent / "data" / "processed" / "beta" / "beta - sub dir" / "beta - sub dir - general.md"
        )
        self.assertEqual(expected, doc.target_path)

    def test_readme_in_root_no_version(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed",
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "readme.md", "")
        rules.rename_uniquely_for_confluence(context, doc)
        expected = Path(__file__).parent / "data" / "processed" / "readme.md"
        self.assertEqual(expected, doc.target_path)

    def test_path_is_confluence_style_true_with_version_name(self):
        root_directory = Path(__file__).parent / "data" / "docs"
        version_name = "testing"
        sub_dir = root_directory / version_name / f"{version_name} - sub dir"
        cases = [
            root_directory / version_name / f"{version_name}.md",
            root_directory / version_name / f"{version_name} - other.md",
            sub_dir / f"{version_name} - sub dir.md",
            sub_dir / f"{version_name} - sub dir - other.md",
            sub_dir / f"{version_name} - sub dir - sub dir 2" / f"{version_name} - sub dir - sub dir 2.md",
            sub_dir / f"{version_name} - sub dir - sub dir 2" / f"{version_name} - sub dir - sub dir 2 - other.md",
        ]
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                self.assertTrue(rules.path_is_confluence_style(root_directory, case, version_name))

    def test_path_is_confluence_style_true_without_version_name(self):
        root_directory = Path(__file__).parent / "data" / "docs"
        version_name = ""
        cases = [
            root_directory / "readme.md",
            root_directory / "other.md",
            root_directory / "sub dir" / "sub dir.md",
            root_directory / "sub dir" / "sub dir - other.md",
            root_directory / "sub dir" / "sub dir - sub dir 2" / "sub dir - sub dir 2.md",
            root_directory / "sub dir" / "sub dir - sub dir 2" / "sub dir - sub dir 2 - other.md",
        ]
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                self.assertTrue(rules.path_is_confluence_style(root_directory, case, version_name))

    def test_path_is_confluence_style_false_with_version_name(self):
        root_directory = Path(__file__).parent / "data" / "docs"
        version_name = "testing"
        cases = [
            root_directory / "readme.md",
            root_directory / "other.md",
            root_directory / "sub dir" / "readme.md",
            root_directory / "sub dir" / "other.md",
            root_directory / "sub dir" / "sub dir 2" / "readme.md",
            root_directory / "sub dir" / "sub dir 2" / "other.md",
        ]
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                self.assertFalse(rules.path_is_confluence_style(root_directory, case, version_name))

    def test_path_is_confluence_style_false_without_version_name(self):
        root_directory = Path(__file__).parent / "data" / "docs"
        version_name = ""
        cases = [
            root_directory / "sub dir" / "readme.md",
            root_directory / "sub dir" / "other.md",
            root_directory / "sub dir" / "sub dir 2" / "readme.md",
            root_directory / "sub dir" / "sub dir 2" / "other.md",
        ]
        for i, case in enumerate(cases):
            with self.subTest(i=i):
                self.assertFalse(rules.path_is_confluence_style(root_directory, case, version_name))


if __name__ == "__main__":
    unittest.main()
