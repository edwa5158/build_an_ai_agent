"""Schema definitions for function calling.

These declarations are used to expose callable tools to the model via
`google.genai.types.FunctionDeclaration`.
"""

import inspect
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file at the specified file path relative to the working directory. Very long results are truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory",
            ),
        },
        required=[
            "file_path",
        ],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to the file at the specified file path within the working directory. If the file and parent directory do not exist within the working directory, it creates them.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the target file.",
            ),
        },
        required=[
            "file_path",
            "content",
        ],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file, with the provided arguments (if provided) and returns the output (if any) as a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="An OPTIONAL array of strings to provide as the inputs to the python function being executed.",
            ),
        },
        required=[
            "file_path",
        ],
    ),
)
