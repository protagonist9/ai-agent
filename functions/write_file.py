import os
from google.genai import types


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
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file with the given content within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)