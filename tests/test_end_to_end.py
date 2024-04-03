# WARNING - these are end-to-end tests
import os
import unittest
import tempfile

from mddocformatter.scripts import cli
from pathlib import Path


@unittest.skipUnless(
    os.environ.get("UNITTEST_END_TO_END", None) is not None,
    "Skipping all end-to-end tests. Define the UNITTEST_END_TO_END environment variable to include them.",
)
class TestLoading(unittest.TestCase):
    def test_process_test_docs_confluence_style(self):
        with tempfile.TemporaryDirectory(prefix="mddocformatter") as tempdir:
            cli.run(
                [
                    "--input",
                    str(Path(__file__).parent / "data" / "docs"),
                    "--output",
                    tempdir,
                    "--style",
                    "confluence",
                    "--version",
                    "test",
                ]
            )
            files = list(Path(tempdir).glob("**/*.*"))
            self.assertEqual(4, len(files))

    def test_process_test_docs_github_style(self):
        with tempfile.TemporaryDirectory(prefix="mddocformatter") as tempdir:
            cli.run(
                [
                    "--input",
                    str(Path(__file__).parent / "data" / "docs"),
                    "--output",
                    tempdir,
                    "--style",
                    "github",
                    "--version",
                    "test",
                ]
            )
            files = list(Path(tempdir).glob("**/*.*"))
            self.assertEqual(4, len(files))


if __name__ == "__main__":
    os.environ["UNITTEST_END_TO_END"] = "true"
    unittest.main()
