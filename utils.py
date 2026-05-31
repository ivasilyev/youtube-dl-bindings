import os
import time
from typing import Any, Dict, Optional

import requests
from jinja2 import Template
from jsonpath_ng import parse

from configs import ConfigurationManager
from constants import BINARY_DIR
from log import log

_config = ConfigurationManager()


def fetch_json_with_retry(url: str, max_attempts: int = None,
                          delay: int = None) -> Optional[Dict[str, Any]]:
    """
    Fetches a webpage as JSON with up to 5 attempts using a for loop.
    """
    if max_attempts is None:
        max_attempts = _config.get_fetch_max_attempts()
    if delay is None:
        delay = _config.get_fetch_max_delay_seconds()

    log.info(f"Fetch url: '{url}'")
    for attempt in range(1, max_attempts + 1):
        try:
            log.info(f"Fetch JSON for attempt {attempt} of {max_attempts}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Success: Parse and return the JSON
            return response.json()

        except requests.exceptions.RequestException as e:
            log.debug(f"Attempt {attempt} failed: {e}")
        except ValueError:
            log.debug(f"Attempt {attempt} failed: Content is not valid JSON.")
            # If the server returned non-JSON, retrying immediately might not help,
            # but we continue the loop in case it was a temporary server error page.

        # Wait before retrying, except after the final attempt
        if attempt < max_attempts:
            time.sleep(delay)

    log.info("All attempts failed. Could not fetch JSON.")
    return None


def get_dict_value_by_jsonpath(d: dict, jsonpath: str):
    jsonpath_expr = parse(jsonpath)
    for match in jsonpath_expr.find(d):
        return match.value


def fetch_latest_tag_name(repository: str) -> str:
    url = f"https://api.github.com/repos/{repository}/releases"
    d: dict = fetch_json_with_retry(url)
    tag_name = get_dict_value_by_jsonpath(d=d, jsonpath="$.[0].tag_name")
    log.info(f"The latest tag name for the repository '{repository}': '{tag_name}'")
    return tag_name


def fetch_binary_with_retry(url: str, file: str, max_attempts: int = None,
                            delay: int = None) -> Optional[str]:
    """
    Fetches a web binary file as raw bytes with up to 5 attempts using a for loop.

    Args:
        url: The direct URL to the binary file.
        file: The downloaded binary file.
        max_attempts: Maximum number of retry attempts.
        delay: Wait time in seconds between retries.

    Returns:
        The raw bytes of the file if successful, or None if all attempts fail.
    """
    if max_attempts is None:
        max_attempts = _config.get_fetch_max_attempts()
    if delay is None:
        delay = _config.get_fetch_max_delay_seconds()

    log.info(f"Fetch url: '{url}'")
    for attempt in range(1, max_attempts + 1):
        try:
            log.info(f"Fetch binary file for attempt {attempt} of {max_attempts}...")

            # Use stream=True to avoid loading large files into memory immediately
            response = requests.get(url, timeout=15, stream=True)
            response.raise_for_status()

            # Success: Write the raw binary content
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, "wb") as f:
                for data in response.iter_content():
                    f.write(data)
                f.close()
                log.info(f"Downloaded: '{file}'")
                return file

        except requests.exceptions.RequestException as e:
            log.debug(f"Attempt {attempt} failed: {e}")

        # Wait before retrying, except after the final attempt
        if attempt < max_attempts:
            time.sleep(delay)

    log.info("All attempts failed. Could not fetch the binary file.")
    return None


def download_latest_github_release(repository: str, file: str):
    log.info(f"Download {repository}")
    release_tag = fetch_latest_tag_name(repository)
    url = f"https://github.com/{repository}/releases/download/{release_tag}/{file}"
    fetch_binary_with_retry(url=url, file=os.path.join(BINARY_DIR, file))


# tests


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


def render_template(template_string: str, values_dict: dict) -> str:
    template = Template(template_string)
    result = template.render(**values_dict)
    return result


def quote_string(s: str):
    s1 = s.strip("'").strip('"')
    return '"' + s1 + '"'


if __name__ == '__main__':
    # fetch_json_with_retry_test()
    # fetch_latest_tag_name_test()
    # fetch_binary_with_retry_test()
    download_latest_github_release_test()
