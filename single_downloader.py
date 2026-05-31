from argparse import ArgumentParser
from typing import Tuple

from arch_based_data_provider import get_yt_dlp_bin
from config import ConfigurationManager
from log import log
from system_utils import run_external_program, ProgramExecutionDto
from utils import render_template, quote_string

_cfg = ConfigurationManager()


def single_download(url: str, directory: str) -> ProgramExecutionDto:
    log.info(f"Download video URL '{url}' into directory '{directory}'")
    template = _cfg.get_single_download_template()
    bin = get_yt_dlp_bin()
    values_dict = dict(
        bin=quote_string(bin),
        url=quote_string(url),
        directory=quote_string(directory),
    )
    command = render_template(template_string=template, values_dict=values_dict)
    return run_external_program(command=command)


def parse_args() -> Tuple[str, str]:
    # 1. Create the parser object
    parser: ArgumentParser = ArgumentParser(description="Single video downloader.")

    # 2. Add the two required arguments
    parser.add_argument("-u", "--url", help="Single video URL")
    parser.add_argument("-d", "--dir", help="Directory to download")

    # 3. Parse the arguments from the CLI
    args = parser.parse_args()
    return args.url, args.dir


def args_based_run():
    url, directory = parse_args()
    single_download(url=url, directory=directory)


# tests


def single_download_test():
    url = "https://www.youtube.com/watch?v=zqTwOoElxBA"  # WOW
    directory = "/tmp"
    #
    single_download(url=url, directory=directory)


if __name__ == '__main__':
    # single_download_test()
    args_based_run()
