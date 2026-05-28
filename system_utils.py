import os


def is_windows_os() -> bool:
    """Returns True if the current operating system is Windows."""
    return os.name == "nt"