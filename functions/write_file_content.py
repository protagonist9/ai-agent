import os
def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(full_path)
    if os.path.isabs(file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    dir_name = os.path.dirname(full_path)
    with open(full_path, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'