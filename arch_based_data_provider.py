from constants import DEFAULT_SINGLE_DOWNLOAD_CMD_TEMPLATE, DEFAULT_PLAYLIST_DOWNLOAD_CMD_TEMPLATE
from system_utils import is_windows_os


def get_youtube_dl_kwargs() -> dict:
    if is_windows_os():
        return dict(repository="ytdl-org/youtube-dl", file="youtube-dl.exe")
    else:
        return dict(repository="ytdl-org/youtube-dl", file="youtube-dl")


def get_yt_dlp_kwargs() -> dict:
    if is_windows_os():
        return dict(repository="yt-dlp/yt-dlp", file="yt-dlp.exe")
    else:
        return dict(repository="yt-dlp/yt-dlp", file="yt-dlp")


def get_quickjs_kwargs() -> dict:
    if is_windows_os():
        return dict(repository="quickjs-ng/quickjs", file="qjs-windows-x86_64.exe")
    else:
        return dict(repository="quickjs-ng/quickjs", file="qjs-linux-x86_64")


def get_ffmpeg_args() -> tuple:
    repo = "BtbN/FFmpeg-Builds"
    if is_windows_os():
        return (repo, "ffmpeg-master-{release_tag}-win64-gpl.zip")
    return (repo, "ffmpeg-master-{release_tag}-linux64-gpl.tar.xz")


def get_deno_args() -> tuple:
    if is_windows_os():
        return ("denoland/deno", "deno-x86_64-pc-windows-msvc.zip")
    else:
        return ("denoland/deno", "deno-x86_64-unknown-linux-gnu.zip")


def get_bun_args() -> tuple:
    if is_windows_os():
        return ("oven-sh/bun", "bun-windows-x64-baseline-profile.zip")
    else:
        return ("oven-sh/bun", "bun-linux-x64-baseline-profile.zip")


def get_default_single_download_cmd() -> str:
    if is_windows_os():
        return DEFAULT_SINGLE_DOWNLOAD_CMD_TEMPLATE.replace("{{ bin }}", "yt-dlp.exe")
    else:
        return DEFAULT_SINGLE_DOWNLOAD_CMD_TEMPLATE.replace("{{ bin }}", "yt-dlp")


def get_default_playlist_download_cmd() -> str:
    if is_windows_os():
        return DEFAULT_PLAYLIST_DOWNLOAD_CMD_TEMPLATE.replace("{{ bin }}", "yt-dlp.exe")
    else:
        return DEFAULT_PLAYLIST_DOWNLOAD_CMD_TEMPLATE.replace("{{ bin }}", "yt-dlp")
