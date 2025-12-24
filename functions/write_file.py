import os
from functions.get_files_info import validate_directory_path

def write_file(working_directory, file_path, content):
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
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))