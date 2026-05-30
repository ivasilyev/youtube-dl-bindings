from config import ConfigurationManager
from log import log
from system_utils import sanitize_command, run_external_program
from utils import render_template

_cfg = ConfigurationManager()


def single_download(url: str, directory: str):
    log.info(f"Download video URL '{url}' into directory '{directory}'")
    template = _cfg.get_single_download_template()
    command = sanitize_command(render_template(template_string=template, values_dict=dict(url=url, directory=directory)))
    run_external_program(command=command)


# tests


def single_download_test():
    url = "https://www.youtube.com/watch?v=zqTwOoElxBA"  # WOW
    directory = "/tmp"
    #
    single_download(url=url, directory=directory)


if __name__ == '__main__':
    single_download_test()
