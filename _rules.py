import os
import functools

from typing import Callable
from fnmatch import fnmatch
from ._consts import PASSES
from ._processing import ProcessingContext
from ._document import Document
from ._utils import format_markdown_link, load_consts_from_py_file


class _DocumentRule(object):
    def __init__(self, function: Callable[[ProcessingContext, Document], None], file_filter: str, pass_index: PASSES):
        """
        Function decorator to create a document processor function. These functions will be called by a
        ProcessingContext to apply augmentations to a file that is loaded in memory.
        :param function: The function being decorated as a document processor.
        :param file_filter: fnmatch style file filter.
        :param pass_index: The index of the "pass" of the documents in which to operate. Sometimes rules need to wait
                           for other rules to run first.
        """
        self.function = function
        self.file_filter = file_filter
        functools.update_wrapper(self, self.function)

    def _applies(self, document: Document):
        fnmatch(document.input_path, self.file_filter)

    def __call__(self, context: ProcessingContext, document: Document):
        if self._applies(document):
            self.function(context, document)


def DocumentRule(
    file_filter: str = "*.*", pass_index: PASSES = PASSES.FIRST
) -> Callable[[Callable[[ProcessingContext, Document], None]], _DocumentRule]:
    """
    A wrapper to make simple DocumentRules from functions.
    :param file_filter: fnmatch style file filter string.
    :param pass_index: The index of the "pass" of the documents in which to operate. Sometimes rules need to wait for
                       other rules to run first.
    :return: A document rule type.
    """

    def _inner(func):
        return _DocumentRule(func, file_filter, pass_index)

    return _inner


@DocumentRule("*.md")
def create_table_of_contents(context: ProcessingContext, document: Document):
    """
    Create a table of contents wherever the document has the variable ${create_table_of_contents}
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    TABLE_OF_CONTENTS_VARIABLE = "${create_table_of_contents}"
    lines = document.contents.split("\n")
    processed = []
    for i, line in enumerate(lines):
        if TABLE_OF_CONTENTS_VARIABLE in line:
            table = []
            for remaining_line in map(lambda x: x.strip(), lines[i + 1 :]):
                if remaining_line.startswith("#"):
                    stripped = remaining_line.lstrip("#").strip()
                    indent_size = max(0, len(remaining_line) - len(remaining_line.lstrip("#")) - 1)
                    table.append(
                        "{} - {}".format("  " * indent_size, format_markdown_link(stripped, "#{}".format(stripped)))
                    )
            line = line.replace(TABLE_OF_CONTENTS_VARIABLE, "\n".join(table))
        processed.append(line)
    document.contents = "\n".join(processed)


@DocumentRule("*.md")
def replace_variables(context: ProcessingContext, document: Document):
    """
    Load a set of consts from the consts file set in the context settings and replace all variables in document
    which are in the form ${some_variable}. The consts file should only contain const values or functions which
    take the document as an argument and return some constant.
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    consts = load_consts_from_py_file(context.settings.consts)
    for key, value in consts.items():
        document.contents = document.contents.replace("${{}}".format(key), str(value))


@DocumentRule("*.md")
def santize_internal_links(context: ProcessingContext, document: Document):
    """
    Find any "internal" markdown links and make sure they use the form ()[<path to item>]
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    pass  # TODO: fill this in


@DocumentRule()
def move_to_target_dir_relative(context: ProcessingContext, document: Document):
    """
    Move the target_path file to save a document to, to the same place under the target_path directory.
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    if context.settings.target_directory and context.settings.root_directory != context.settings.target_directory:
        rel_path = os.path.relpath(context.settings.root_directory, document.input_path)
        document.target_path = os.path.join(context.settings.target_directory, rel_path)


@DocumentRule("*.md")
def rename_uniquely_for_confluence(context: ProcessingContext, document: Document):
    """
    Renames each page so that it contains its own tree as part of its name for the purpose of making the file
    uniquely named. This is to comply with the need in confluence for all pages to have unique names. This also
    renames "README.md" files after their parent directory.

    This will also place the version_name as the root directory.
    So, given a page:
      - "something/else/aswell.md
    this rule will rename it to
      - "develop/something/else/something - else - aswell.md
    :param context: The ProcessingContext.
    :param document: The document being processed.
    """
    rel_path = os.path.relpath(context.settings.root_directory, document.input_path)
    rel_path = rel_path.replace(".md", "")  # remove file extension, we know it's .md
    parts = [context.settings.version_name] + rel_path.split(os.path.sep)
    parent_dir = os.path.dirname(os.path.dirname(rel_path))
    basename = os.path.basename(document.input_path)
    if basename.lower() == "readme.md" or basename == f"{parent_dir}.md":
        parts = parts[:-1] + [" - ".join(parts[:-1]) + ".md"]
    else:
        parts = parts[:-1] + [" - ".join(parts) + ".md"]
    context.target = os.path.join(context.settings.target_directory, *parts)
