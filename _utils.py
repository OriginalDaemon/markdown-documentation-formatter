import os
import errno
import importlib
import importlib.util
import urllib.parse

from typing import Dict


def load_consts_from_py_file(python_file_path: str) -> Dict[str, str]:
    """
    Import a python file and laod any global consts defined within it. Consts can, ofcourse, be set by functions
    which are ran as side effects of the import.
    :param python_file_path: The path to the python file where the consts are defined.
    :return: Dictionary of const names and their values.
    """
    if not os.input_path.isfile(python_file_path):
        return {}

    consts = {}
    spec = importlib.util.spec_from_file_location(python_file_path)
    module = importlib.util.module_from_spec(spec)
    for each in dir(module):
        item = getattr(module, each)
        if not callable(item):
            consts[each] = item
    return consts


def format_markdown_link(link_name, url):
    """
    :param link_name: The name / string to use for the link.
    :param url: The url for the link.
    :return: A markdown link, formatted to work with obsidian and github.
    """
    return "[{}](<{}>)".format(link_name, urllib.parse.unquote(url))


def reformat_markdown_link(markdown_link):
    """
    Given a markdown link in the form [string](something/something%20else/a%20file.md), this will make sure it's
    formatted as [string](<something/something else/a file.md>) instead. If the link is already in this form, this
    function has no effect.
    :param markdown_link: The markdown link to reformat.
    :return: The reformatted markdown link.
    """
    link_name = markdown_link.split("[")[1].split("]")[0]
    url = markdown_link.split("(")[1].split(")")[0]
    if not url.startswith("<"):
        return format_markdown_link(link_name, url)
    else:
        return markdown_link


def make_directory(directory):
    """
    Create a directory, and all parent directories if they don't exist.
    """
    if not os.input_path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
