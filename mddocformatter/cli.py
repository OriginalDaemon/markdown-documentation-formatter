import pathlib
import argparse
import logging

from typing import Tuple, List, Dict

from mddocformatter import (
    DeploymentStyle,
    process_docs,
    validate_docs,
    loading,
    rules,
    DocumentRule,
    FunctionMacro,
)


def _process_path_arg(path, arg_name, expect_exists=True, expect_dir=False):
    if not path:
        raise argparse.ArgumentTypeError("{}: value can't be blank.".format(arg_name))

    path = pathlib.Path(path).resolve()
    if expect_exists and not path.exists():
        raise argparse.ArgumentTypeError("{}: doesn't exist: {}".format(arg_name, path))
    if path.exists() and expect_dir != path.is_dir():
        if expect_dir:
            raise argparse.ArgumentTypeError("{}: directory expected, got a file: {}".format(arg_name, path))
        else:
            raise argparse.ArgumentTypeError("{}: file expected, got a directory: {}".format(arg_name, path))
    return path


def _deploymentStyle(value):
    for t in list(DeploymentStyle):
        if value == t.value:
            return t
    raise argparse.ArgumentTypeError("Deployment type invalid: {}".format(value))


def parse_args(
    argv: list | None = None,
) -> Tuple[pathlib.Path, pathlib.Path, List[DocumentRule], Dict[str, str], Dict[str, FunctionMacro], str, bool, bool]:
    """
    Parse the command line args.
    :param argv: argument list from the command line.
    :return: tuple of the parsed args:
               - input file relative_path
               - output relative_path
    """
    parser = argparse.ArgumentParser(description="Convert basic obj/collada/fbx/usd meshes to Gr2")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the directory containing the docs to prep.",
        type=lambda x: _process_path_arg(x, "input", True, True),
    )
    group.add_argument(
        "--output",
        "-o",
        required=False,
        default=None,
        help="Directory to output the prepared documentation to. If not given, the output results will override the "
        "input instead.",
        type=lambda x: _process_path_arg(x, "output", False, True),
    )
    parser.add_argument(
        "--style",
        "-s",
        default=DeploymentStyle.CONFLUENCE,
        help="Determines the default ruleset to use. Use confluence|github to use rule-sets applicable for deployment "
        "to the respective platforms. Use custom to only use rules provided via the --rules argument.",
        type=_deploymentStyle,
    )
    parser.add_argument(
        "--macros",
        "-m",
        default=None,
        help="The location of the macros file.",
        type=lambda x: _process_path_arg(x, "macros", True, False),
    )
    parser.add_argument(
        "--rules",
        "-r",
        default=None,
        help="The location of the rules module with your custom rules in it.",
        type=lambda x: _process_path_arg(x, "rules", True, False),
    )
    parser.add_argument("--version", default="", help="The name to use for the version of the documentation.")
    group.add_argument(
        "--validate",
        required=False,
        default=False,
        help="Processes the documentation in a validation mode. This will report if the documentation already meats "
        "the requirements for the given style or not.",
        action="store_true",
    )
    parser.add_argument("--verbose", "-v", default=False, help="Use verbose logging", action="store_true")
    args = parser.parse_args(argv)

    rule_set = rules.GetRulesForStyle(args.style)

    if args.style == DeploymentStyle.CUSTOM and args.rules is None:
        parser.error("You must provide a module with custom rules to use the custom deployment style.")

    if args.rules is not None:
        rule_set.extend(loading.load_custom_rules_from_py_file(args.rules))

    const_macros: Dict[str, str] = {}
    function_macros: Dict[str, FunctionMacro] = {}
    if args.macros is not None:
        const_macros, function_macros = loading.load_macros_from_py_file(args.macros)

    output = args.output
    if args.output is None:
        output = args.input

    return args.input, output, rule_set, const_macros, function_macros, args.version, args.validate, args.verbose


def run(argv: list | None = None) -> bool:
    """
    Takes a folder of documentation and prepares it for deployment in various ways.
    """
    input_dir, output_dir, rule_set, const_macros, function_macros, version_name, validate, verbose = parse_args(argv)
    logging.basicConfig(
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.DEBUG if verbose else logging.INFO
    )
    if not validate:
        return process_docs(input_dir, output_dir, rule_set, const_macros, function_macros, version_name)
    else:
        return validate_docs(input_dir, rule_set, const_macros, function_macros, version_name)
