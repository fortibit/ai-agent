import os


def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_path)
    
    # Validate if the path is within working directory
    if not abs_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check if the directory argument is a directory
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    try:
        return build_metadata_str(abs_path, directory)
    except Exception as e:
        return f"Error listing files: {e}"


def build_metadata_str(abs_path, directory):
    # file metadata tuples (str file/dir name, int size, bool isdir)
    files_info = []

    # list of strings, one per file
    # Add standard string
    if directory == ".":
        files_str = [f"Result for current directory:"]
    else:
        files_str = [f"Result for '{directory}' directory:"]

    # List filenames
    dir_content = os.listdir(abs_path)

    # Join filenames with their full path
    dir_content_paths = list(map(lambda filename: os.path.join(abs_path, filename), dir_content))

    # Get info for each file in current path
    for filepath in dir_content_paths:
        files_info.append((filepath.split("/")[-1], os.path.getsize(filepath), os.path.isdir(filepath)))

    # Convert data into string
    for file in files_info:
        files_str.append(f" - {file[0]}: file_size={file[1]} bytes, is_dir={file[2]}")

    # Files_info one per line
    return "\n".join(files_str)
    