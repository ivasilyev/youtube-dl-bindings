import os
import subprocess
from typing import List, Tuple

from log import log


def is_windows_os() -> bool:
    """Returns True if the current operating system is Windows."""
    return os.name == "nt"


def run_external_program(command: str, timeout: int = 30) -> Tuple[str, str, int]:
    """
    Executes an external program and returns its stdout, stderr, and exit code.

    Args:
        command: A string representing the command and its arguments.
                 Example: "ls -la" or "python3 --version"
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
            timeout=timeout,  # Prevents the script from hanging indefinitely,
            shell=True,
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


def run_external_program_test():
    print(run_external_program('echo "aaaa bbb ccc'))
    # print(subprocess.getoutput('C:/Windows/system32/cmd.exe -c echo "aaaa bbb ccc"'))
    # print(subprocess.getoutput('echo "aaaa bbb ccc"'))


if __name__ == '__main__':
    run_external_program_test()
