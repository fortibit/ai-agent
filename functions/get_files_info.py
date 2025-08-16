import os
import sys


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_path)
    
    # Validate if the path is within working directory
    if working_directory not in abs_path.split("/")[-2:]:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check if the directory argument is a directory
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    
    return build_metadata_str(abs_path)


def build_metadata_str(abs_path):

    return f""
    