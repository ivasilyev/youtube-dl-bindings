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


