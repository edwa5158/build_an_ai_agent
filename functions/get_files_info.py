import os 

def get_files_info(working_directory, directory = "."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if directory == ".":
            result = "Result for current directory:"
        else: 
            result = f"Result for '{directory}' directory:"
        
        if not valid_target_dir:
            result = "\n".join([result, f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'])
            return result
        if not os.path.isdir(target_dir):
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