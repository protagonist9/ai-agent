import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not (absolute_file_path == absolute_working_dir or absolute_file_path.startswith(absolute_working_dir + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", absolute_file_path]
    if args is not None:
        command.extend(args)


    try:
        result = subprocess.run(
            command,
            cwd=absolute_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:{result.stderr}")

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"