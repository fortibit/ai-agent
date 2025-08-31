import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir, full_path = check_path(working_directory, file_path)
    except Exception as e:
        return e
    try:
        commands = ["python", full_path] + args
        completed_process = subprocess.run(
            commands, timeout=30, capture_output=True, text=True, cwd=abs_working_dir
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    return format_output(completed_process)


def format_output(process):
    process_returncode = process.returncode
    process_stdout = process.stdout
    process_stderr = process.stderr
    if not process_stdout and not process_stderr:
        return "No output produced"
    if process_returncode != 0:
        return f"Process exited with code {process_returncode}"
    return f"STDOUT:\n{process_stdout}\n\nSTDERR:\n{process_stderr}"


def check_path(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        raise Exception(
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        )
    if not file_path.endswith(".py"):
        raise Exception(f'Error: "{file_path} is not a Python file.')
    if not os.path.exists(file_path):
        raise Exception(f'Error: File "{file_path}" not found.')
    return abs_working_dir, abs_file_path
