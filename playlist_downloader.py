import os
import tempfile
from typing import List

from config import ConfigurationManager
from constants import ENCODING_UTF8
from file_system_utils import find_files
from io_utils import load_lines
from log import log
from single_downloader import single_download
from system_utils import sanitize_command, run_external_program
from utils import render_template

_cfg = ConfigurationManager()


def check_id_in_directory(video_id: str, directory: str):
    files: List[str] = find_files(directory)
    for file in files:
        if video_id in os.path.basename(file):
            log.debug("Video ID '{video_id}' found in '{directory}'")
            return True
    log.debug("Video ID '{video_id}' not found in '{directory}'")
    return False


def playlist_download(playlist_url: str, directory: str):
    template = _cfg.get_playlist_download_template()
    temp_file: tempfile._TemporaryFileWrapper = tempfile.NamedTemporaryFile(
        mode='w+',
        encoding=ENCODING_UTF8,
        delete=False
    )
    file = temp_file.name
    # Close it right away to handle the "open" command later
    temp_file.close()
    values_dict = dict(url=playlist_url, file=file)
    command = sanitize_command(render_template(template_string=template, values_dict=values_dict))
    try:
        run_external_program(command=command)
        log.info(f"Saved video IDs to temporary file: '{file}'")
        lines: List[str] = load_lines(file)
        counter = 0
        for line in lines:
            video_id = line.strip()
            if check_id_in_directory(video_id=video_id, directory=directory):
                log.info(f"Skip ID '{video_id}'")
                continue
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            single_download(url=video_url, directory=directory)
            counter += 1
        log.info(f"Processed {counter} IDs")
    finally:
        os.remove(file)
        log.info(f"Removed temporary file with video IDs: '{file}'")


# tests


def playlist_download_test():
    url = "https://www.youtube.com/watch?v=zqTwOoElxBA"  # WOW
    directory = "/tmp"
    #
    playlist_download(playlist_url=url, directory=directory)


if __name__ == '__main__':
    playlist_download_test()
