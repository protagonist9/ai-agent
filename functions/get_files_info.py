import os
from google import genai
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a directory and shows their sizes.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory to list, relative to the working directory.",
            ),
        },
    ),
) 

def get_files_info(working_directory, directory="."):
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        lines = []

        for name in os.listdir(target_dir):
            full_path = os.path.join(target_dir, name)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)
            lines.append(f'- {name}: file_size={size} bytes, is_dir={is_dir}')
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

