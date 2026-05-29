import os
from collections import deque
from typing import List

from log import log


def extract_zip_recursively(zip_path: str, extract_to: str) -> None:
    """
    Extracts a ZIP archive into a directory, and recursively extracts
    any nested ZIP files found inside.
    """
    import zipfile
    # 1. Extract the main root ZIP archive
    log.info(f"Extract file '{zip_path}' into '{extract_to}'")
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


def extract_tar_gz_recursively(tar_path: str, extract_to: str) -> None:
    """
    Extracts a .tar.gz archive into a directory, and recursively extracts
    any nested .tar.gz files found inside.
    """
    import tarfile
    # 1. Extract the main root tar.gz archive
    with tarfile.open(tar_path, "r:gz") as tar_ref:
        tar_ref.extractall(path=extract_to, filter="data")

    # 2. Use a loop to scan for newly extracted inner tar.gz files
    tar_found = True
    while tar_found:
        tar_found = False

        for root, dirs, files in os.walk(extract_to):
            for file in files:
                # Check for common extensions: .tar.gz or .tgz
                if file.lower().endswith(('.tar.gz', '.tgz')):
                    current_tar_path = os.path.join(root, file)

                    # Create a specific folder name for the nested tar content
                    # Example: "archive.tar.gz" extracts into "archive/"
                    if file.lower().endswith('.tar.gz'):
                        folder_name = file[:-7]  # Strip .tar.gz
                    else:
                        folder_name = file[:-4]  # Strip .tgz

                    nested_extract_to = os.path.join(root, folder_name)

                    # Extract the nested archive
                    with tarfile.open(current_tar_path, "r:gz") as tar_ref:
                        tar_ref.extractall(path=nested_extract_to, filter="data")

                    # Clean up and delete the internal archive file after unpacking it
                    os.remove(current_tar_path)

                    # Signal the loop to scan again since new tar files might have appeared
                    tar_found = True
                    break  # Break out to refresh os.walk with the new file structure
            if tar_found:
                break


def extract_tar_xz_recursively(tar_path: str, extract_to: str) -> None:
    """
    Extracts a .tar.xz archive into a directory, and recursively extracts
    any nested .tar.xz or .txz files found inside.
    """
    import tarfile
    # 1. Extract the main root tar.xz archive ("r:xz" specifies XZ compression)

    with tarfile.open(tar_path, "r:xz") as tar_ref:
        tar_ref.extractall(path=extract_to, filter="data")

    # 2. Use a loop to scan for newly extracted inner tar.xz files
    tar_found = True
    while tar_found:
        tar_found = False
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                # Check for common extensions: .tar.xz or .txz
                if file.lower().endswith(('.tar.xz', '.txz')):
                    current_tar_path = os.path.join(root, file)

                    # Create a specific folder name for the nested tar content
                    if file.lower().endswith('.tar.xz'):
                        folder_name = file[:-7]  # Strip .tar.xz
                    else:
                        folder_name = file[:-4]  # Strip .txz

                    nested_extract_to = os.path.join(root, folder_name)

                    # Extract the nested archive
                    with tarfile.open(current_tar_path, "r:xz") as tar_ref:
                        tar_ref.extractall(path=nested_extract_to, filter="data")

                    # Clean up and delete the internal archive file after unpacking it
                    os.remove(current_tar_path)

                    # Signal the loop to scan again since new files might have appeared
                    tar_found = True
                    break  # Break out to refresh os.walk with the new file structure
            if tar_found:
                break


def extract_archive(archive: str, directory: str):
    if archive.endswith(".zip"):
        return extract_zip_recursively(zip_path=archive, extract_to=directory)
    if archive.endswith(".tar.gz"):
        return extract_tar_gz_recursively(tar_path=archive, extract_to=directory)
    if archive.endswith(".tar.xz"):
        return extract_tar_xz_recursively(tar_path=archive, extract_to=directory)
    raise ValueError(f"Unknown archive type: '{archive}'")


def find_files(directory: str) -> List[str]:
    out: deque[str] = deque()
    for root, dirs, files in os.walk(directory):
        for file in files:
            out.append(os.path.join(root, file))
    return sorted(out)