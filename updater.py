import os
import shutil

from arch_based_data_provider import get_youtube_dl_kwargs, get_yt_dlp_kwargs, get_quickjs_kwargs, get_ffmpeg_args, \
    get_deno_args
from file_system_utils import extract_zip_recursively, find_files
from log import log
from utils import download_latest_github_release, fetch_latest_tag_name, fetch_binary_with_retry, BINARY_DIR


def download_ffmpeg():
    repository, template = get_ffmpeg_args()
    release_tag = fetch_latest_tag_name(repository)
    file = template.format(release_tag=release_tag)
    url = f"https://github.com/{repository}/releases/download/{release_tag}/{file}"
    archive = os.path.join(BINARY_DIR, file)
    fetch_binary_with_retry(url=url, file=archive)
    extract_to = os.path.join(BINARY_DIR, "ffmpeg")
    extract_zip_recursively(zip_path=archive, extract_to=extract_to)
    bin_dir = os.path.join(extract_to, "bin")
    for file in find_files(bin_dir):
        basename = os.path.basename(file)
        shutil.move(file, os.path.join(BINARY_DIR, basename))
    log.info("Cleanup")
    os.remove(archive)
    shutil.rmtree(extract_to)


def download_deno():
    repository, file = get_deno_args()
    download_latest_github_release(repository=repository, file=file)
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
