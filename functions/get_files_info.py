import os 

def get_files_info(working_directory: str, directory: str = "."):
    try:
        target_dir, valid_target_dir, is_dir, _ = validate_directory_path(working_directory, directory)
        if directory == ".":
            result = "Result for current directory:"
        else: 
            result = f"Result for '{directory}' directory:"
        
        if not valid_target_dir:
            result = "\n".join([result, f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'])
            return result
        if not is_dir:
            result = "\n".join([result,  f'    Error: "{directory}" is not a directory'])
            return result

        
        for dir in os.listdir(target_dir):
            dir_path = os.path.join(target_dir, dir)
            is_dir = os.path.isdir(dir_path)
            filesize = os.path.getsize(dir_path)
            current_file = f"  - {dir}: file_size={filesize} bytes, is_dir={is_dir}"
            result = "\n".join([result, current_file])
        return result
    
    except Exception as e:
        return f"Error: {e}"

def validate_directory_path(working_directory: str, directory: str)->tuple[str, bool, bool, bool]:
    """
    Docstring for validate_directory_path
    
    :param working_directory: The working directory to search for a file or directory
    :type working_directory: str
    :param directory: The directory (or file name) to search for in the `working_directory`
    :type directory: str
    :return: 
            - `target_dir` - the absolute path to the specified `directory` in `working_directory`\n
            - `valid_taret_dir` - if the `directory` is within the `working_directory`\n
            - `is_dir` - if `directory` is a directory (False if `valid_target_dir` = False)\n
            - `is_file` - if `directory` is a file (False if `valid_target_dir` = False)
    :rtype: tuple[str, bool, bool, bool]
    """
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    is_dir = os.path.isdir(target_dir) and valid_target_dir
    is_file = os.path.isfile(target_dir) and valid_target_dir
    return target_dir, valid_target_dir, is_dir, is_file


if __name__ == "__main__":
    result = get_files_info("calculator", "../")
    print(result)