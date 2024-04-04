import difflib

from pathlib import Path
from ._consts import N_CONTEXT_LINES_IN_DIFF


class Document(object):
    def __init__(self, input_path: Path, data: str = ""):
        """
        Holds a file, referenced by relative_path, and it's contents, for manipulation by document rule_set.
        :param input_path: The relative_path to the input file.
        """
        self.input_path: Path = input_path
        self.target_path: Path = Path(input_path)
        self._original_contents: str = data
        self.contents: str = data

    @property
    def unchanged(self) -> bool:
        """
        :return: True if the document is currently unchanged compared to its original contents.
        """
        return self._original_contents == self.contents

    def changes(self, n_context_lines=N_CONTEXT_LINES_IN_DIFF) -> str:
        """
        Get a description of the changes between the original content when the document was loaded and the current
        contents. If there are no changes, this function returns an empty string.
        :param n_context_lines: The number of "context" lines to show above+below a change.
        :return: A string describing the difference between the original document contents and the current contents.
        """

        if not self.unchanged:
            a = self._original_contents.split("\n")
            b = self.contents.split("\n")
            result = ""
            for text in difflib.unified_diff(a, b, n=n_context_lines):
                if text[:3] not in ("+++", "---", "@@ "):
                    result += text + "\n"
            return result
        else:
            return ""
