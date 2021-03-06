import datetime as dt
import os
from pathlib import Path
from typing import Tuple, List

import pandas as pd

from util.functionalLib.functional import foldl, append
from util.lib.timeConverter import time_converter


def create_filename(t: Tuple[dt.datetime, dt.datetime], file: str) -> str:
    """
    Creates a file name with correct timestamp and file extension for .csv files
    :param t: Tuple that cointains start timestamp and end timestamp of the processed data
    :param file: File that we want to give an file extension
    :return: file with file extension
        Example: test.csv changes to test__2021-01-01_03:00:00__2021-01-01_03:59:59.csv
    """
    return file[:-4] \
           + '__' + time_converter(t[0].timestamp()) \
           + '__' + time_converter(t[1].timestamp() - 1 / 10 ** 6) + '.csv'


def create_dirs(full_path: str) -> None:
    """
    Create a new directory at this given path. Any missing parents of this path are created as needed; they are created
    with the default permissions. Nested directory will only be created if it does not exist.
    :param full_path: Path where the directory should be created
    :return: None/Void
    """
    Path(full_path).mkdir(parents=True, exist_ok=True)


def save_data(df: pd.DataFrame, dst_dir: str, file_name: str, sub_dirs: List[str] = None) -> None:
    """
    Stores DataFrame in given destination directory inside the passed subdirectory
    :param df: DataFrame to be stored
    :param dst_dir: Destination directory
    :param file_name: Filename
    :param sub_dirs: Subdirectories where data should be stored. If nonexistent they will be created automatically
        Notes:
         - if sub_dirs = [''] => does the same as sub_dirs = None
         - undefined behaviour if sub_dirs = []
    :return: None/Void
    """
    if sub_dirs:
        full_path: str = foldl(join_path, dst_dir, sub_dirs)
        create_dirs(full_path)
        df.to_csv(os.path.join(full_path, file_name), index=False)
    else:
        df.to_csv(os.path.join(dst_dir, file_name), index=False)


def join_path(current_path: str, sub_dir: str) -> str:
    """
    Joins to paths
    :param current_path: Parent path
    :param sub_dir: Subdirectory of parent
    :return:New path containing current_path as root and sub_dir as subdirectory
    """
    return os.path.join(current_path, sub_dir)


def walk_dirs(root: str) -> None:
    """
    Walks through every directory in root recursively and prints directories and filenames
    :param root:Root directory we want to walsk through
    :return: None/Void
    """
    for root, subdirs, files in os.walk(root):
        print(f'--\nroot = {root}')

        for subdir in subdirs:
            print(f'\t- subdirectory {subdir}')

        for filename in files:
            file_path = os.path.join(root, filename)
            print(f'\t- file {filename} (full path: {file_path})')


def find_files_recursive(root: str, ends_with: str) -> List[str]:
    """
    Finds all files with given file ending in root directory and all its subdirectories
    :param root: Path to root folder
    :param ends_with: File extension of files we want to filter
    :return: List of all files in root directory and subdirectories with given file ending
    """
    result: List[str] = []
    for _, _, files in os.walk(root):
        result = foldl(
            append,
            result,
            filter(
                lambda x: os.fsdecode(filename=x).endswith(ends_with),
                files
            )
        )
    return result
