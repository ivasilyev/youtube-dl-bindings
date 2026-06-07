import os
from argparse import ArgumentParser
from collections import deque
from datetime import timedelta
from math import floor
from typing import Tuple, Optional, List

import m3u8
from pydantic import BaseModel

from arch_based_data_provider import get_ffprobe_bin
from constants import BINARY_DIR
from file_system_utils import find_files_by_extension, find_files_by_extension_list
from io_utils import dump_string
from log import log
from system_utils import run_external_program, ProgramExecutionDto
from utils import quote_string, safe_find_regex, remove_empty_values


def run_ffprobe(file: str) -> str:
    ffprobe_bin = get_ffprobe_bin()
    command = f"{quote_string(ffprobe_bin)} -i {quote_string(file)} -show_format -v quiet"
    dto: ProgramExecutionDto = run_external_program(command=command)
    log.info(dto)
    return dto.stdout


def get_delta(file: str) -> Optional[timedelta]:
    s: str = run_ffprobe(file)
    duration = safe_find_regex(regex="duration=([.0-9\r\n]+)", string=s).strip()
    if len(duration) > 0:
        delta: timedelta = timedelta(seconds=float(duration))
        return delta


class FilterDto(BaseModel):
    extensions: List[str]
    max_duration: timedelta


def find_matching_files(directory: str, dto: FilterDto):
    files: List[str] = find_files_by_extension_list(directory=directory, extensions=dto.extensions)
    queue: deque[str] = deque()
    for file in files:
        delta: timedelta = get_delta(file)
        if delta is None:
            continue
        if delta > dto.max_duration:
            continue
        # more checks
        queue.append(file)
    return list(queue)


def create_m3u_file(m3u_file: str, media_files: List[str]):
    playlist: m3u8.M3U8 = m3u8.M3U8()
    for file in media_files:
        delta: timedelta = get_delta(file)
        track = m3u8.Segment(
            uri=file,
            title=os.path.basename(file),
            duration=floor(delta.total_seconds()),
        )
        playlist.segments.append(track)
    dump_string(string=playlist.dumps(), file=m3u_file)


def parse_args() -> Tuple[str, str, int]:
    # 1. Create the parser object
    parser: ArgumentParser = ArgumentParser(description="Single video downloader.")

    # 2. Add the two required arguments
    parser.add_argument("-i", "--dir", help="Input directory")
    parser.add_argument("-u", "--m3u", help="Output file")
    parser.add_argument("-d", "--max_duration", help="Maximal duration in seconds to filter")

    # 3. Parse the arguments from the CLI
    args = parser.parse_args()
    return args.dir, args.m3u, args.max_duration


if __name__ == '__main__':
    pass
