from config import ConfigurationManager
from system_utils import sanitize_command
from utils import render_template

_cfg = ConfigurationManager()


def single_download(url: str, directory: str):
    template = _cfg.get_yt_dlp_command_template()
    cmd = sanitize_command(render_template(template_string=template, values_dict=dict(url=url, directory=directory)))
    print(cmd)


# tests


def single_download_test():
    url = "https://www.youtube.com/watch?v=zqTwOoElxBA"  # WOW
    directory = "/tmp"
    #
    single_download(url=url, directory=directory)


if __name__ == '__main__':
    single_download_test()
