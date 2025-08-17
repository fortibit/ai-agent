import os
from config import *


def get_file_content(working_directory, file_path):
    # Create absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.join(abs_working_dir, file_path)

    # Check for errors
    error = check_path(abs_working_dir, abs_file_path, file_path)

    try:
        # Get file contents
        return read_file(abs_file_path)
    except Exception as e:
        return f"Error: {e}"

def check_path(abs_working_dir_path, abs_file_path, file_path):
    if not abs_file_path.startswith(abs_working_dir_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    pass


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(f.read()) > MAX_CHARS:
            file_content_string += f'[...File "{file_path.split("/")[-1]}" truncated at {MAX_CHARS} characters]'
        return file_content_string