import os

from arch_based_data_provider import get_ffmpeg_args, \
    get_deno_args, get_bun_args, get_quickjs_kwargs, get_youtube_dl_kwargs, get_yt_dlp_kwargs
from file_system_utils import extract_archive, find_files, get_basename_without_all_extensions, \
    move_recursively, remove_recursively
from log import log
from utils import download_latest_github_release, fetch_latest_tag_name, BINARY_DIR, fetch_binary_with_retry


def download_ffmpeg():
    repository, template = get_ffmpeg_args()
    release_tag = fetch_latest_tag_name(repository)
    file = template.format(release_tag=release_tag)
    url = f"https://github.com/{repository}/releases/download/{release_tag}/{file}"
    archive = os.path.join(BINARY_DIR, file)
    fetch_binary_with_retry(url=url, file=archive)
    extract_to = os.path.join(BINARY_DIR, "ffmpeg")
    extract_archive(archive=archive, directory=extract_to)
    bin_dir = os.path.join(extract_to, get_basename_without_all_extensions(archive), "bin")
    files = find_files(bin_dir)
    for file in files:
        basename = os.path.basename(file)
        move_recursively(bin_dir, os.path.join(BINARY_DIR, basename))
    log.info("Cleanup")
    remove_recursively(archive)
    remove_recursively(extract_to)


def download_deno():
    repository, file = get_deno_args()
    download_latest_github_release(repository=repository, file=file)
    archive = os.path.join(BINARY_DIR, file)
    extract_to = os.path.join(BINARY_DIR, "deno")
    extract_archive(archive=archive, directory=extract_to)
    log.info("Cleanup")
    remove_recursively(archive)
    remove_recursively(extract_to)


def download_bun():
    repository, file = get_bun_args()
    download_latest_github_release(repository=repository, file=file)
    archive = os.path.join(BINARY_DIR, file)
    extract_to = os.path.join(BINARY_DIR, "bun")
    extract_archive(archive=archive, directory=extract_to)
    files = find_files(extract_to)
    for file in files:
        basename = os.path.basename(file)
        move_recursively(file, os.path.join(BINARY_DIR, basename))
    log.info("Cleanup")
    remove_recursively(archive)
    remove_recursively(extract_to)


def download():
    # youtube-dl
    download_latest_github_release(**get_youtube_dl_kwargs())
    # yt-dlp
    download_latest_github_release(**get_yt_dlp_kwargs())
    # ffmpeg
    download_ffmpeg()
    # deno
    download_deno()
    # quickjs
    download_latest_github_release(**get_quickjs_kwargs())
    # bun
    download_bun()


if __name__ == '__main__':
    download()
