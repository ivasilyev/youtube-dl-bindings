import os

ROOT_DIR = os.getcwd()
BINARY_DIR = os.path.join(ROOT_DIR, "bin")
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")

# Default values
DEFAULT_YT_DLP_CMD_TEMPLATE = """
"{{ bin }} \
    --abort-on-unavailable-fragment \
    --mtime \
    --embed-chapters \
    --embed-metadata \
    --min-sleep-interval=60 \
    --max-sleep-interval=90 \
    --sleep-interval=15 \
    --sleep-requests=3 \
    --sleep-subtitles=3 \
    --cookies-from-browser=${cookiesBrowser} \
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
    --output={{ directory }}/%(title)s__%(id)s.%(ext)s \
    --verbose \
    {{ url }}
"""
