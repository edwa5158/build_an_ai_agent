"""Contains the function `write_file` to write text files within a validated working directory."""

import os
from functions.function_utils import validate_directory_path

def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Write text content to a file path within the permitted working directory.
    
    :param working_directory: Base directory that bounds where writes are allowed.
    :type working_directory: str
    :param file_path: Relative path (from the working directory) of the file to write.
    :type file_path: str
    :param content: Text content to write to the target file.
    :type content: str
    :return: A human-readable status message indicating success or the reason for failure.
    :rtype: str
    """
    try:
        target_dir, valid_target_dir, is_dir, is_file = validate_directory_path(working_directory, file_path)

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(target_dir.removesuffix(file_path), exist_ok=True)
        with open(target_dir, 'wt') as f:
            chars_written = f.write(content)
        
        if chars_written > 0:
            return f'Successfully wrote to "{file_path}" ({chars_written} characters written)'
        else:
            return f'No characters were written to {file_path}...for some reason'
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
