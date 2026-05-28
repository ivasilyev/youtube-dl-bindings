import os
import shutil

from log import log
from utils import download_latest_github_release, fetch_latest_tag_name, fetch_binary_with_retry, BINARY_DIR, \
    extract_zip_recursively, find_files


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
    download_latest_github_release(repository="ytdl-org/youtube-dl", file="youtube-dl.exe")
    # yt-dlp
    download_latest_github_release(repository="yt-dlp/yt-dlp", file="yt-dlp.exe")
    # FFmpeg
    download_ffmpeg()
    # deno
    download_deno()
    # quickjs
    download_latest_github_release(repository="quickjs-ng/quickjs", file="qjs-windows-x86_64.exe")


if __name__ == '__main__':
    download()
