from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists file and directory names in a folder. Only shows names, NOT file contents. Use get_file_content to read file contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Path to the directory to list, relative to the working directory",
            ),
        },
        required=[],
    ),
)