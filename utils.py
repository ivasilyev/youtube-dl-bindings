import os
import subprocess
import time
import zipfile
from collections import deque
from typing import Any, Dict, Optional, List, Tuple

import requests
from jsonpath_ng import parse

from log import log

BINARY_DIR = os.path.join(os.getcwd(), "bin")


def fetch_json_with_retry(url: str, max_attempts: int = 5, delay: int = 2) -> Optional[Dict[str, Any]]:
    """
    Fetches a webpage as JSON with up to 5 attempts using a for loop.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            log.info(f"Attempt {attempt} of {max_attempts}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Success: Parse and return the JSON
            return response.json()

        except requests.exceptions.RequestException as e:
            log.info(f"Attempt {attempt} failed: {e}")
        except ValueError:
            log.info(f"Attempt {attempt} failed: Content is not valid JSON.")
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
    return get_dict_value_by_jsonpath(d=d, jsonpath="$.[0].tag_name")


def fetch_binary_with_retry(url: str, file: str, max_attempts: int = 5, delay: int = 2) -> Optional[str]:
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
    for attempt in range(1, max_attempts + 1):
        try:
            log.info(f"Attempt {attempt} of {max_attempts}...")

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
            log.info(f"Attempt {attempt} failed: {e}")

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


def extract_zip_recursively(zip_path: str, extract_to: str) -> None:
    """
    Extracts a ZIP archive into a directory, and recursively extracts
    any nested ZIP files found inside.
    """
    # 1. Extract the main root ZIP archive
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # 2. Use a loop to scan for newly extracted inner ZIP files
    # os.walk is used to find nested files at any depth level
    ziplist_found = True
    while ziplist_found:
        ziplist_found = False

        for root, dirs, files in os.walk(extract_to):
            for file in files:
                if file.lower().endswith('.zip'):
                    current_zip_path = os.path.join(root, file)

                    # Create a specific folder name for the nested zip content
                    # Example: "archive.zip" extracts into a folder named "archive/"
                    folder_name = os.path.splitext(file)[0]
                    nested_extract_to = os.path.join(root, folder_name)

                    # Extract the nested ZIP file
                    with zipfile.ZipFile(current_zip_path, 'r') as zip_ref:
                        zip_ref.extractall(nested_extract_to)

                    # Clean up and delete the internal ZIP file after unpacking it
                    os.remove(current_zip_path)

                    # Signal the loop to scan again since new ZIPs might have appeared
                    ziplist_found = True
                    break  # Break out to refresh os.walk with the new file structure
            if ziplist_found:
                break


def find_files(directory: str) -> List[str]:
    out: deque[str] = deque()
    for root, dirs, files in os.walk(directory):
        for file in files:
            out.append(os.path.join(root, file))
    return sorted(out)


def run_external_program(command: List[str], timeout: int = 30) -> Tuple[str, str, int]:
    """
    Executes an external program and returns its stdout, stderr, and exit code.

    Args:
        command: A list of strings representing the command and its arguments.
                 Example: ["ls", "-la"] or ["python3", "--version"]
        timeout: Maximum time in seconds to wait for the program to complete.

    Returns:
        A tuple containing (stdout_string, stderr_string, return_code)
    """
    try:
        # Run the command securely using a list of arguments (avoids shell=True)
        result = subprocess.run(
            command,
            capture_output=True,  # Captures both stdout and stderr
            text=True,  # Automatically decodes bytes to string (UTF-8)
            check=False,  # Prevents throwing an error on non-zero exit codes
            timeout=timeout  # Prevents the script from hanging indefinitely
        )

        return result.stdout, result.stderr, result.returncode

    except subprocess.TimeoutExpired as e:
        log.info(f"Error: The command timed out after {timeout} seconds.")
        # Return what was captured before the timeout occurred
        stdout = e.stdout.decode('utf-8') if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = e.stderr.decode('utf-8') if isinstance(e.stderr, bytes) else (e.stderr or "")
        return stdout, stderr, -1

    except FileNotFoundError:
        log.info(f"Error: The executable '{command[0]}' was not found.")
        return "", f"Executable '{command[0]}' not found.", -1


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


if __name__ == '__main__':
    # fetch_json_with_retry_test()
    # fetch_latest_tag_name_test()
    # fetch_binary_with_retry_test()
    download_latest_github_release_test()
