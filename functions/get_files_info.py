import os 
from functions.function_utils import validate_directory_path

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

if __name__ == "__main__":
    result = get_files_info("calculator", "../")
    print(result)