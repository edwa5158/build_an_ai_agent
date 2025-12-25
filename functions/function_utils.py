"""Shared utility helpers for function implementations."""

import os 

def validate_directory_path(working_directory: str, directory: str)->tuple[str, bool, bool, bool]:
    """
    Docstring for validate_directory_path
    
    :param working_directory: The working directory to search for a file or directory
    :type working_directory: str
    :param directory: The directory (or file name) to search for in the `working_directory`
    :type directory: str
    :return: A tuple containing basic info about the file / directory and if it's valid.

            - `target_dir` - the absolute path to the specified `directory` in `working_directory`
            - `valid_taret_dir` - if the `directory` is within the `working_directory`
            - `is_dir` - if `directory` is a directory (False if `target_is_valid` = False)
            - `is_file` - if `directory` is a file (False if `target_is_valid` = False)
    :rtype: tuple[str, bool, bool, bool]
    """
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    target_is_valid = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    is_dir = os.path.isdir(target_dir) and target_is_valid
    is_file = os.path.isfile(target_dir) and target_is_valid
    return target_dir, target_is_valid, is_dir, is_file
