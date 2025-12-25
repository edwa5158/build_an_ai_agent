"""Safely execute Python files located within a validated working directory."""

from functions.function_utils import validate_directory_path
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """
    Execute a Python file with optional arguments.
    
    :param working_directory: The base working directory for file validation
    :type working_directory: str
    :param file_path: The path to the Python file to execute
    :type file_path: str
    :param args: Optional list of arguments to pass to the Python script
    :type args: list[str] | None
    :return: The output or error message from the executed script
    :rtype: str
    """
    try:
        target_dir, target_is_valid, is_dir, is_file = validate_directory_path(
            working_directory, file_path
        )

        if not target_is_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if is_dir:
            return f'Error: Cannot execute "{file_path}" as it is a directory'
        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        python = ".venv/bin/python"

        command: list[str] = [python, target_dir]
        if args:
            command.extend(args)

        sub = subprocess.run(command, capture_output=True, text=True, timeout=30)
        result: str = ""
        if sub.returncode != 0:
            result = f"Process exited with code {sub.returncode}"
        if not (sub.stderr or sub.stdout):
            result = "\n".join([result, "No output produced"])
        else:
            result = "\n".join(
                [result, f"STDOUT: {sub.stdout}", f"STDERR: {sub.stderr}"]
            )

        return result

    except Exception as e:
        return f"Error: {e}"

def __parse_inputs__():
    """Parse CLI arguments for the `run_python_file` module.

    :return: Parsed CLI arguments with `working_dir`, `file_path`, and optional `args`.
    :rtype: argparse.Namespace
    """
    import argparse
    parser = argparse.ArgumentParser(description="run_python_file")
    parser.add_argument("working_dir", type=str, help="Working directory")
    parser.add_argument("file_path", type=str, help="Python file to run")
    parser.add_argument(
        "--args",
        nargs=argparse.REMAINDER,
        default=None,
        help="OPTIONAL: the args you want to pass to the script called",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = __parse_inputs__()
    print(run_python_file(args.working_dir, args.file_path, args.args))

