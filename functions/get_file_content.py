import os

#                    "calculator"     , "pkg/calculator.py"
#                    "calculator"     , "main.py"
#                    "calculator"     , "/bin/cat"               <== error str
#                    "calculator"     , "pkg/does_not_exist.py"  <== error str
def get_file_content(working_directory, file_path):
    # Create absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.join(abs_working_dir, file_path)

    return check_path(abs_working_dir, abs_file_path, file_path)


def check_path(abs_working_dir_path, abs_file_path, file_path):
    if not abs_file_path.startswith(abs_working_dir_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    pass