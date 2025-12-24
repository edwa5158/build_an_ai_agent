import config
from functions.function_utils import validate_directory_path

def get_file_content(working_directory, file_path):        
    try:
        target_dir, valid_target_dir, is_dir, is_file = validate_directory_path(working_directory, file_path)

        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_dir, 'rt') as f:
            content: str = f.read(config.MAX_CHARACTERS_TO_READ)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARACTERS_TO_READ} characters]'
        return content
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(get_file_content("calculator", "lorem.txt"))