import os

from constants import BINARY_DIR
from log import log
from playlist_downloader import playlist_download
from single_downloader import single_download
from system_utils import run_external_program
from utils import fetch_json_with_retry, fetch_latest_tag_name, fetch_binary_with_retry, download_latest_github_release


def test_playlist_download():
    url = "https://www.youtube.com/playlist?list=PLmBK9jc1368IfTwX0Vf3G_6GROJYc2XrH"
    directory = "/tmp"
    #
    playlist_download(playlist_url=url, directory=directory)


def test_single_download():
    url = "https://www.youtube.com/watch?v=zqTwOoElxBA"  # WOW
    directory = "/tmp"
    #
    single_download(url=url, directory=directory)


def run_external_program_test():
    cmd = """
echo \
"aaa \
bbb \
ccc"
"""
    #
    log.info(run_external_program(cmd).stdout)


def fetch_json_with_retry_test():
    url = "https://api.github.com/repos/ytdl-org/youtube-dl/releases"
    #
    d: dict = fetch_json_with_retry(url)
    log.info(d)


def fetch_latest_tag_name_test():
    repository = "ytdl-org/youtube-dl"
    #
    latest_tag_name = fetch_latest_tag_name(repository=repository)
    log.info(latest_tag_name)


def fetch_binary_with_retry_test():
    file = "youtube-dl.exe"
    #
    fetch_binary_with_retry(
        url=f"https://github.com/ytdl-org/youtube-dl/releases/download/2021.12.17/{file}",
        file=os.path.join(BINARY_DIR, file)
    )


def download_latest_github_release_test():
    repository = "ytdl-org/youtube-dl"
    file = "youtube-dl.exe"
    #
    download_latest_github_release(repository=repository, file=file)