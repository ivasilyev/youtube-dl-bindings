from arch_based_data_provider import get_yt_dlp_bin
from config import ConfigurationManager
from log import log
from system_utils import run_external_program
from utils import render_template, quote_string

_cfg = ConfigurationManager()


def single_download(url: str, directory: str):
    log.info(f"Download video URL '{url}' into directory '{directory}'")
    template = _cfg.get_single_download_template()
    bin = get_yt_dlp_bin()
    values_dict = dict(
        bin=quote_string(bin),
        url=quote_string(url),
        directory=quote_string(directory),
    )
    command = render_template(template_string=template, values_dict=values_dict)
    run_external_program(command=command)


# tests


def single_download_test():
    url = "https://www.youtube.com/watch?v=zqTwOoElxBA"  # WOW
    directory = "/tmp"
    #
    single_download(url=url, directory=directory)


if __name__ == '__main__':
    single_download_test()
