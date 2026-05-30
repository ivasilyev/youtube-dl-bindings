import os
import subprocess

from pydantic import BaseModel

from log import log


class ProgramExecutionDto(BaseModel):
    """
    A simplified replacement for subprocess.CompletedProcess
    """
    stdout: str
    stderr: str
    success: bool


def is_windows_os() -> bool:
    """Returns True if the current operating system is Windows."""
    return os.name == "nt"


def run_external_program(command: str, timeout: int = None) -> ProgramExecutionDto:
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
        result: subprocess.CompletedProcess = subprocess.run(
            command,
            capture_output=True,  # Captures both stdout and stderr
            text=True,  # Automatically decodes bytes to string (UTF-8)
            check=False,  # Prevents throwing an error on non-zero exit codes
            timeout=timeout,  # Prevents the script from hanging indefinitely,
            shell=True,
        )
        return ProgramExecutionDto(stdout=result.stdout, stderr=result.stderr, success=result.returncode == 0)

    except subprocess.TimeoutExpired as e:
        log.info(f"Error: The command timed out after {timeout} seconds.")
        # Return what was captured before the timeout occurred
        stdout = e.stdout.decode('utf-8') if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = e.stderr.decode('utf-8') if isinstance(e.stderr, bytes) else (e.stderr or "")
        return ProgramExecutionDto(stdout=stdout, stderr=stderr, success=False)

    except FileNotFoundError:
        log.info(f"Error: The executable was not found.")
        return ProgramExecutionDto(stdout="", stderr="Executable not found.", success=False)


# tests


def run_external_program_test():
    log.info(run_external_program('echo "aaaa bbb ccc"').stdout)


if __name__ == '__main__':
    run_external_program_test()
