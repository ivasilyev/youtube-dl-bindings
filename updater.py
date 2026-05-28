import os
import shutil

from arch_based_data_provider import get_youtube_dl_kwargs, get_yt_dlp_kwargs, get_quickjs_kwargs
from log import log
from utils import download_latest_github_release, fetch_latest_tag_name, fetch_binary_with_retry, BINARY_DIR
from file_system_utils import extract_zip_recursively, find_files


def download_ffmpeg():
    repository = "BtbN/FFmpeg-Builds"
    release_tag = fetch_latest_tag_name(repository)
    folder = f"ffmpeg-master-{release_tag}-win64-gpl"
    file = f"{folder}.zip"
    url = f"https://github.com/{repository}/releases/download/{release_tag}/{file}"
    archive = os.path.join(BINARY_DIR, file)
    fetch_binary_with_retry(url=url, file=archive)
    extract_to = os.path.join(BINARY_DIR, folder)
    extract_zip_recursively(zip_path=archive, extract_to=extract_to)
    bin_dir = os.path.join(extract_to, "bin")
    for file in find_files(bin_dir):
        basename = os.path.basename(file)
        shutil.move(file, os.path.join(BINARY_DIR, basename))
    log.info("Cleanup")
    os.remove(archive)
    shutil.rmtree(extract_to)


def download_deno():
    file = "deno-x86_64-pc-windows-msvc.zip"
    download_latest_github_release(repository="denoland/deno", file=file)
    archive = os.path.join(BINARY_DIR, file)
    extract_zip_recursively(zip_path=archive, extract_to=BINARY_DIR)
    os.remove(archive)


def download_bun():
    folder = "bun-windows-x64-baseline-profile"
    file = f"{folder}.zip"
    download_latest_github_release(repository="oven-sh/bun", file=file)
    archive = os.path.join(BINARY_DIR, file)
    extract_zip_recursively(zip_path=archive, extract_to=BINARY_DIR)
    os.remove(archive)


def download():
    # youtube-dl
    download_latest_github_release(**get_youtube_dl_kwargs())
    # yt-dlp
    download_latest_github_release(**get_yt_dlp_kwargs())
    # FFmpeg
    download_ffmpeg()
    # deno
    download_deno()
    # quickjs
    download_latest_github_release(**get_quickjs_kwargs())


if __name__ == '__main__':
    download()
