import unittest

from pathlib import Path
from mddocproc import ProcessingSettings, ProcessingContext, Document, rules


class TestMoveToTargetDirRelative(unittest.TestCase):
    def test_move_root_dir_file(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed"
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "test.md", "")
        rules.move_to_target_dir_relative(context, doc)

        self.assertEqual(Path(__file__).parent / "data" / "processed" / "test.md", doc.target_path)

    def test_move_sub_dir_file(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed"
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "sub dir" / "test.md", "")
        rules.move_to_target_dir_relative(context, doc)

        self.assertEqual(Path(__file__).parent / "data" / "processed" / "sub dir" / "test.md", doc.target_path)

    def test_move_sub_dir_file_with_version_name(self):
        settings = ProcessingSettings(
            root_directory=Path(__file__).parent / "data" / "docs",
            target_directory=Path(__file__).parent / "data" / "processed",
            version_name="beta"
        )
        context = ProcessingContext(settings)
        doc = Document(Path(__file__).parent / "data" / "docs" / "sub dir" / "test.md", "")
        rules.move_to_target_dir_relative(context, doc)

        self.assertEqual(Path(__file__).parent / "data" / "processed" / "beta" / "sub dir" / "test.md", doc.target_path)
