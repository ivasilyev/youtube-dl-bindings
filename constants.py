import os

ENCODING_UTF8 = "utf-8"

ROOT_DIR = os.getcwd()
BINARY_DIR = os.path.join(ROOT_DIR, "bin")
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")

# Default values
DEFAULT_SINGLE_DOWNLOAD_CMD_TEMPLATE = """
{{ bin }} \
    --abort-on-unavailable-fragment \
    --mtime \
    --embed-chapters \
    --embed-metadata \
    --min-sleep-interval=60 \
    --max-sleep-interval=90 \
    --sleep-interval=15 \
    --sleep-requests=3 \
    --sleep-subtitles=3 \
    --match-filter=!is_live \
    --no-skip-unavailable-fragments \
    --no-abort-on-unavailable-fragments \
    --no-skip-unavailable-fragments \
    --no-check-certificates \
    --retries=100 \
    --fragment-retries=100 \
    --add-metadata \
    --all-subs \
    --convert-subs=ass \
    --embed-subs \
    --format=bestvideo+bestaudio/best \
    --preset-alias=mkv \
    --merge-output-format=mkv \
    --remux-video=mkv \
    --js-runtimes='deno:.' \
    --js-runtimes='bun:.' \
    --js-runtimes='quickjs:.' \
    --ffmpeg-location=. \
    --output={{ directory }}/'%(title)s__%(id)s.%(ext)s' \
    --verbose \
    {{ url }}
"""
# --proxy=socks5://127.0.0.1:1080
# --cookies-from-browser firefox:~/snap/firefox/common/.mozilla/firefox/

DEFAULT_PLAYLIST_DOWNLOAD_CMD_TEMPLATE = """
{{ bin }} \
    --ignore-errors \
    --flat-playlist \
    --print-to-file=%(id)s \
    {{ file }} \
    {{ url }}
"""
