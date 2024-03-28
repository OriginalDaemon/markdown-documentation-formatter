import sys
import pathlib
import argparse

from . import DeploymentStyle, ProcessDocs
from ._utils import load_consts_from_py_file


def _process_path_arg(path, arg_name, expect_exists=True, expect_dir=False):
    if not path:
        raise argparse.ArgumentTypeError("{}: value can't be blank.".format(arg_name))

    path = pathlib.Path(path)
    if expect_exists and not path.exists():
        raise argparse.ArgumentTypeError(
            "{}: path doesn't exist: {}".format(arg_name, path)
        )
    if path.exists() and expect_dir != path.is_dir():
        if expect_dir:
            return argparse.ArgumentTypeError(
                "{}: directory expected, got a file: {}".format(arg_name, path)
            )
        else:
            return argparse.ArgumentTypeError(
                "{}: file expected, got a directory: {}".format(arg_name, path)
            )
    return path


def _deploymentStyle(value):
    for t in list(DeploymentStyle):
        if value == t:
            return t
    raise argparse.ArgumentTypeError("Deployment type invalid: {}".format(value))


def parseArgs(argv: list | None = None):
    """
    Parse the command line args.
    :param argv: argument list from the command line.
    :return: tuple of the parsed args:
               - input file path
               - output path
    """
    parser = argparse.ArgumentParser(
        description="Convert basic obj/collada/fbx/usd meshes to Gr2"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the directory containing the docs to prep.",
        type=lambda x: _process_path_arg(x, "input", True, True),
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Directory to output the prepared documentation to.",
        type=lambda x: _process_path_arg(x, "output", False, True),
    )
    parser.add_argument(
        "--style",
        "-s",
        default=DeploymentStyle.CONFLUENCE,
        help="The style of deployment to do.",
        type=_deploymentStyle,
    )
    parser.add_argument(
        "--consts",
        "-c",
        default=None,
        help="The location of the consts file.",
        type=lambda x: _process_path_arg(x, "consts", True, False),
    )
    parser.add_argument(
        "--version",
        "-v",
        default="",
        help="The name to use for the version of the documentation.",
    )
    args = parser.parse_args(argv)

    consts = {}
    if args.consts is not None:
        consts = load_consts_from_py_file(args.consts)

    return args.input, args.output, args.type, consts, args.version


def main():
    """
    Takes a folder of documentation and prepares it for deployment in various ways.
    """
    return ProcessDocs(*parseArgs(sys.argv[1:]))


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
