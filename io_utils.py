import re
from typing import List

from constants import ENCODING_UTF8
from log import log


def load_string(file: str) -> str:
    with open(file, "r", encoding=ENCODING_UTF8) as file:
        s = file.read()
    log.info(f"Loaded: '{file}'")
    return s


def load_lines(file: str) -> List[str]:
    s = load_string(file)
    return re.split("[\n\r]", s)


def dump_string(string: str, file: str) -> None:
    with open(file, "w", encoding=ENCODING_UTF8) as f:
        f.write(string)
        f.close()
    log.info(f"Saved: '{file}'")
