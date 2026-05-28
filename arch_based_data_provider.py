from system_utils import is_windows_os


def get_youtube_dl_kwargs() -> dict:
    if is_windows_os():
        return dict(repository="ytdl-org/youtube-dl", file="youtube-dl.exe")
    else:
        return


def get_yt_dlp_kwargs() -> dict:
    if is_windows_os():
        return dict(repository="yt-dlp/yt-dlp", file="yt-dlp.exe")
    else:
        return


def get_quickjs_kwargs() -> dict:
    if is_windows_os():
        return dict(repository="quickjs-ng/quickjs", file="qjs-windows-x86_64.exe")
    else:
        return


def get_ffmpeg_args() -> tuple:
    repo = "BtbN/FFmpeg-Builds"
    if is_windows_os():
        return (repo, "ffmpeg-master-{release_tag}-win64-gpl.zip")
    return (repo, "ffmpeg-master-{release_tag}-linux64-gpl.tar.xz")


def get_deno_args() -> tuple:
    if is_windows_os():
        return ("denoland/deno", "deno-x86_64-pc-windows-msvc.zip")
    else:
        return
