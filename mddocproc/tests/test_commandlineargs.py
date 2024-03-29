import os
import pathlib
import unittest

from mddocproc.scripts import cli
from mddocproc import rules
from mddocproc import DeploymentStyle
from unittest.mock import patch


class TestCommandLineArgs(unittest.TestCase):
    def test_no_args(self):
        with self.assertRaises(SystemExit):
            cli.parse_args([])

    def test_only_output_and_input_given(self):
        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir") as mock_is_dir:
                mock_exists.return_value = True
                mock_is_dir.return_value = True
                cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])

    def test_input_invalid(self):
        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir") as mock_is_dir:
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    mock_is_dir.return_value = True
                    cli.parse_args(["--input", "", "--output", "output_file_path"])

    def test_input_notexists(self):
        def _exists(v):
            return v.name != "input_file_path"

        with patch.object(pathlib.Path, "exists", new=_exists):
            with patch.object(pathlib.Path, "is_dir") as mock_is_dir:
                with self.assertRaises(SystemExit):
                    mock_is_dir.return_value = True
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])

    def test_input_notadir(self):
        def _is_dir(v):
            return v.name != "input_file_path"

        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir", new=_is_dir):
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])

    def test_output_notexists(self):
        def _exists(v):
            return v.name != "output_file_path"

        with patch.object(pathlib.Path, "exists", new=_exists):
            with patch.object(pathlib.Path, "is_dir") as mock_is_dir:
                mock_is_dir.return_value = True
                input_dir, output_dir, rule_set, consts, version_name = cli.parse_args(
                    ["--input", "input_file_path", "--output", "output_file_path"]
                )
                self.assertEqual(output_dir, pathlib.Path("output_file_path"))

    def test_output_notadir(self):
        def _is_dir(v):
            return v.name != "output_file_path"

        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir", new=_is_dir):
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])

    def test_use_pathlib_paths(self):
        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                input_dir, output_dir, rule_set, consts, version_name = cli.parse_args(
                    ["--input", "input_file_path", "--output", "output_file_path"]
                )
                self.assertIsInstance(input_dir, pathlib.Path)
                self.assertIsInstance(output_dir, pathlib.Path)

    def test_defaults_expected(self):
        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                input_dir, output_dir, rule_set, consts, version_name = cli.parse_args(
                    ["--input", "input_file_path", "--output", "output_file_path"]
                )
                self.assertListEqual(rule_set, rules.StandardRulesTable[DeploymentStyle.CONFLUENCE])
                self.assertDictEqual(consts, {})
                self.assertEqual(version_name, "")

    def test_github_style(self):
        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                input_dir, output_dir, rule_set, consts, version_name = cli.parse_args(
                    ["--input", "input_file_path", "--output", "output_file_path", "--style", "github"]
                )
                self.assertListEqual(rule_set, rules.StandardRulesTable[DeploymentStyle.GITHUB])

    def test_invalid_style(self):
        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                with self.assertRaises(SystemExit):
                    cli.parse_args(
                        [
                            "--input",
                            "input_file_path",
                            "--output",
                            "output_file_path",
                            "--style",
                            "abcdefghijklmnopqrstuvwxyz",
                        ]
                    )

    def test_consts_file_loading(self):
        def _is_dir(v):
            return not v.name.endswith("consts.py")

        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir", new=_is_dir):
                mock_exists.return_value = True
                input_dir, output_dir, rule_set, consts, version_name = cli.parse_args(
                    [
                        "--input",
                        "input_file_path",
                        "--output",
                        "output_file_path",
                        "--consts",
                        os.path.join(os.path.dirname(__file__), "data", "consts.py"),
                    ]
                )
                self.assertDictEqual(
                    consts,
                    {
                        "author": "hello",
                        "job": "world",
                    },
                )

    def test_consts_file_isdir(self):
        with patch.object(pathlib.Path, "exists") as mock_exists:
            with patch.object(pathlib.Path, "is_dir") as mock_isdir:
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    mock_isdir.return_value = True
                    cli.parse_args(
                        [
                            "--input",
                            "input_file_path",
                            "--output",
                            "output_file_path",
                            "--consts",
                            "consts_file_path.py",
                        ]
                    )

    def test_consts_file_invalid(self):
        def _exists(v):
            return v != "consts_file_path.py"

        with patch.object(pathlib.Path, "exists", new=_exists):
            with patch.object(pathlib.Path, "is_dir") as mock_isdir:
                with self.assertRaises(SystemExit):
                    mock_isdir.return_value = True
                    cli.parse_args(
                        [
                            "--input",
                            "input_file_path",
                            "--output",
                            "output_file_path",
                            "--consts",
                            "consts_file_path.py",
                        ]
                    )


def get_suite():
    tests = [
        unittest.TestLoader().loadTestsFromTestCase(TestCommandLineArgs),
    ]
    return unittest.TestSuite(tests)


def run_tests():
    import sys

    suite = get_suite()
    unittest.TextTestRunner(stream=sys.stderr).run(suite)


if __name__ == "__main__":
    unittest.main()
