import os
from functions.get_file_content import get_file_content

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.join(abs_working_dir, file_path)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Create dir if it doesn't extist
    create_dirs(file_path)

    try:
        # Write content to file
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

def create_dirs(file_path):
    try:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path))
    except Exception as e:
        return f"Error: {e}"