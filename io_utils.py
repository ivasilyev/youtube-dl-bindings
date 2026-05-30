import re
from typing import List

from constants import ENCODING_UTF8


def load_string(file: str) -> str:
    with open(file, "r", encoding=ENCODING_UTF8) as file:
        s = file.read()
    return s


def load_lines(file: str) -> List[str]:
    s = load_string(file)
    return re.split("[\n\r]", s)
