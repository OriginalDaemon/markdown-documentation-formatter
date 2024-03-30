import os
import errno


def format_markdown_link(text: str, relative_path: str, section: str | None = None):
    """
    Creates a well formatted markdown link.
    :param text: The text to display as the markdown link.
    :param relative_path: The relative path to the file you want to link.
    :param section: If provided, this adds the subsection #... part so you can link to a subsection of another file.
    """
    section_part = f"#{section}" if section else ""
    return f"[{text}](<{relative_path}{section_part}>)"


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
