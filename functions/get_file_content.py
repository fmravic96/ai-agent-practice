import os
from google.genai import types
from config import FILE_CHARACTER_LIMIT


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path, "r") as file:
            content = file.read(FILE_CHARACTER_LIMIT + 1)
            if len(content) > FILE_CHARACTER_LIMIT:
                content = (
                    content[:FILE_CHARACTER_LIMIT]
                    + f"[...File \"{file_path}\" truncated at {FILE_CHARACTER_LIMIT} characters]"
                )
            return content
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)
