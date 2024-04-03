import os
import unittest

from pathlib import Path
from mddocformatter import cli
from mddocformatter import rules
from mddocformatter import DeploymentStyle
from unittest.mock import patch


class TestCommandLineArgs(unittest.TestCase):
    def test_no_args(self):
        with self.assertRaises(SystemExit):
            cli.parse_args([])

    def test_only_output_and_input_given(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_is_dir:
                mock_exists.return_value = True
                mock_is_dir.return_value = True
                cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])

    def test_input_invalid(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_is_dir:
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    mock_is_dir.return_value = True
                    cli.parse_args(["--input", "", "--output", "output_file_path"])

    def test_input_notexists(self):
        def _exists(v: Path):
            return v.name != "input_file_path"

        with patch.object(Path, "exists", new=_exists):
            with patch.object(Path, "is_dir") as mock_is_dir:
                with self.assertRaises(SystemExit):
                    mock_is_dir.return_value = True
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])

    def test_input_notadir(self):
        def _is_dir(v: Path):
            return v.name != "input_file_path"

        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir", new=_is_dir):
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])

    def test_output_notexists(self):
        def _exists(v: Path):
            return v.name != "output_file_path"

        with patch.object(Path, "exists", new=_exists):
            with patch.object(Path, "is_dir") as mock_is_dir:
                mock_is_dir.return_value = True
                input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = (
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])
                )
                self.assertEqual(Path("output_file_path"), output_dir)

    def test_output_notadir(self):
        def _is_dir(v: Path):
            return v.name != "output_file_path"

        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir", new=_is_dir):
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])

    def test_use_pathlib_paths(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = (
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])
                )
                self.assertIsInstance(input_dir, Path)
                self.assertIsInstance(output_dir, Path)

    def test_defaults_expected(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = (
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path"])
                )
                self.assertListEqual(rules.GetRulesForStyle(DeploymentStyle.CONFLUENCE), rule_set)
                self.assertDictEqual({}, const_macros)
                self.assertDictEqual({}, function_macros)
                self.assertEqual("", version_name)
                self.assertFalse(validate)

    def test_github_style(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = (
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path", "--style", "github"])
                )
                self.assertListEqual(rules.GetRulesForStyle(DeploymentStyle.GITHUB), rule_set)

    def test_custom_style(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                with self.assertRaises(SystemExit):
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path", "--style", "custom"])

    def test_invalid_style(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_isdir:
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

    def test_macro_file_loading(self):
        def _is_dir(v: Path):
            return not v.name.endswith("macros.py")

        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir", new=_is_dir):
                mock_exists.return_value = True
                input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = (
                    cli.parse_args(
                        [
                            "--input",
                            "input_file_path",
                            "--output",
                            "output_file_path",
                            "--macros",
                            os.path.join(os.path.dirname(__file__), "data", "macros.py"),
                        ]
                    )
                )
                self.assertIn("author", const_macros)
                self.assertEqual("hello", const_macros["author"])
                self.assertIn("title", const_macros)
                self.assertEqual("world", const_macros["title"])
                self.assertIn("capitalize", function_macros)
                self.assertTrue(callable(function_macros["capitalize"]))

    def test_rules_module(self):
        def _is_dir(v: Path):
            return not v.name.endswith("rules.py")

        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir", new=_is_dir):
                mock_exists.return_value = True
                input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = (
                    cli.parse_args(
                        [
                            "--input",
                            "input_file_path",
                            "--output",
                            "output_file_path",
                            "--rules",
                            os.path.join(os.path.dirname(__file__), "data", "rules.py"),
                        ]
                    )
                )
                self.assertTrue(any(x.__name__ == "my_rule" for x in rule_set))
                self.assertEqual(len(rules.GetRulesForStyle(DeploymentStyle.CONFLUENCE)) + 1, len(rule_set))

    def test_rules_module_only_when_using_custom_mode(self):
        def _is_dir(v: Path):
            return not v.name.endswith("rules.py")

        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir", new=_is_dir):
                mock_exists.return_value = True
                input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = (
                    cli.parse_args(
                        [
                            "--input",
                            "input_file_path",
                            "--output",
                            "output_file_path",
                            "--style",
                            "custom",
                            "--rules",
                            os.path.join(os.path.dirname(__file__), "data", "rules.py"),
                        ]
                    )
                )
                self.assertEqual("my_rule", rule_set[0].__name__)
                self.assertEqual(1, len(rule_set))

    def test_consts_file_isdir(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_isdir:
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    mock_isdir.return_value = True
                    cli.parse_args(
                        [
                            "--input",
                            "input_file_path",
                            "--output",
                            "output_file_path",
                            "--macros",
                            "consts_file_path.py",
                        ]
                    )

    def test_consts_file_invalid(self):
        def _exists(v: Path):
            return v != "consts_file_path.py"

        with patch.object(Path, "exists", new=_exists):
            with patch.object(Path, "is_dir") as mock_isdir:
                with self.assertRaises(SystemExit):
                    mock_isdir.return_value = True
                    cli.parse_args(
                        [
                            "--input",
                            "input_file_path",
                            "--output",
                            "output_file_path",
                            "--macros",
                            "consts_file_path.py",
                        ]
                    )

    def test_validate_error_with_output(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_isdir:
                with self.assertRaises(SystemExit):
                    mock_exists.return_value = True
                    mock_isdir.return_value = True
                    cli.parse_args(["--input", "input_file_path", "--output", "output_file_path", "--validate"])

    def test_validate_option(self):
        with patch.object(Path, "exists") as mock_exists:
            with patch.object(Path, "is_dir") as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = (
                    cli.parse_args(["--input", "input_file_path", "--validate"])
                )
                self.assertTrue(validate)


if __name__ == "__main__":
    unittest.main()
