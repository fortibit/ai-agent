import os
from config import *
from google.genai import types


def get_file_content(working_directory, file_path):
    # Create absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        # Get file contents
        return read_file(abs_file_path)
    except Exception as e:
        # Check for errors
        return check_path(abs_working_dir, abs_file_path, file_path, e)


def check_path(abs_working_dir_path, abs_file_path, file_path, e):
    if not abs_file_path.startswith(abs_working_dir_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        return f"Error: {e}"


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        file_content_string = f.read(MAX_CHARS)

        # If the file content is more than MAX_CHARS truncate it and add note
        if len(f.read()) > MAX_CHARS:
            file_content_string += f'[...File "{file_path.split("/")[-1]}" truncated at {MAX_CHARS} characters]'
        return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads specified file in working directory and returns its content as a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to read the content from, relative to the working directory.",
            ),
        },
    ),
)