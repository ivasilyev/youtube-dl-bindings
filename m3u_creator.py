import os
from argparse import ArgumentParser
from datetime import timedelta
from math import floor
from typing import Tuple, Optional, List

import m3u8
from pydantic import BaseModel

from arch_based_data_provider import get_ffprobe_bin
from file_system_utils import ends_with_extension, find_files
from io_utils import dump_string
from log import log
from mp_utils import map_reduce
from system_utils import run_external_program, ProgramExecutionDto
from utils import quote_string, safe_find_regex, remove_empty_values


def run_ffprobe(file: str) -> str:
    log.info(f"Run ffprobe on '{file}'")
    ffprobe_bin = get_ffprobe_bin()
    command = f"{quote_string(ffprobe_bin)} -i {quote_string(file)} -show_format -v quiet"
    dto: ProgramExecutionDto = run_external_program(command=command)
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


class FileInfoDto(BaseModel):
    uri: str
    duration: timedelta


def get_file_info(file: str, filter: FilterDto) -> Optional[FileInfoDto]:
    if all(not ends_with_extension(file=file, extension=i) for i in filter.extensions):
        return
    delta: timedelta = get_delta(file)
    if delta is None:
        return
    if filter.max_duration.total_seconds() > 0 and delta > filter.max_duration:
        return
    # more checks
    dto: FileInfoDto = FileInfoDto(uri=file, duration=delta)
    return dto


def create_m3u_file(m3u_file: str, dtos: List[FileInfoDto]):
    playlist: m3u8.M3U8 = m3u8.M3U8()
    for dto in dtos:
        track = m3u8.Segment(
            uri=dto.uri,
            title=os.path.basename(dto.uri),
            duration=floor(dto.duration.total_seconds()),
        )
        playlist.segments.append(track)
    dump_string(string=playlist.dumps(), file=m3u_file)


def parse_args() -> Tuple[str, str, int, str]:
    # 1. Create the parser object
    parser: ArgumentParser = ArgumentParser(description="Single video downloader.")

    # 2. Add the two required arguments
    parser.add_argument("-i", "--dir", help="Input directory")
    parser.add_argument("-o", "--m3u", help="Output file")
    parser.add_argument("-d", "--max_duration", help="Maximal duration in seconds to filter", type=int, default=0)
    parser.add_argument("-x", "--extensions", help="Comma-separated file extensions", default="mp4,mkv,webm")

    # 3. Parse the arguments from the CLI
    args = parser.parse_args()
    return (
        args.dir,
        args.m3u,
        args.max_duration,
        args.extensions,
    )


def run(
        input_directory: str,
        output_file: str,
        max_duration_seconds: int,
        extension_string: str,
):
    extension_list = remove_empty_values(extension_string.split(","))
    max_duration: timedelta = timedelta(seconds=max_duration_seconds)
    filter_dto: FilterDto = FilterDto(extensions=extension_list, max_duration=max_duration)
    files = find_files(input_directory)
    kwargs_list=[dict(file=i, filter=filter_dto) for i in files]
    raw_file_info_list: List[FileInfoDto] = map_reduce(func=get_file_info, kwargs_list=kwargs_list)
    file_info_list = sorted(remove_empty_values(raw_file_info_list), key=lambda x: x.uri)
    create_m3u_file(m3u_file=output_file, dtos=file_info_list)


if __name__ == '__main__':
    kwargs: tuple = parse_args()
    run(*kwargs)
