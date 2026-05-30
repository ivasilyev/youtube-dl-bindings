from config import ConfigurationManager
from system_utils import sanitize_command, run_external_program
from utils import render_template

_cfg = ConfigurationManager()


def playlist_download(url: str, directory: str):
    template = _cfg.get_playlist_download_template()
    command = sanitize_command(render_template(template_string=template, values_dict=dict(url=url, directory=directory)))
    run_external_program(command=command)


# tests


def playlist_download_test():
    url = "https://www.youtube.com/watch?v=zqTwOoElxBA"  # WOW
    directory = "/tmp"
    #
    playlist_download(url=url, directory=directory)


if __name__ == '__main__':
    playlist_download_test()
