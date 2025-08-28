from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    import os
    import subprocess

    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not full_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        try:
            result = subprocess.run(
                ["python3", full_path] + args,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                return f"Process exited with code {result.returncode}"
            if not result.stdout and not result.stderr:
                return "No output produced."

            return f"STDOUT: {result.stdout} STDERR: {result.stderr}"
        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f"Error: {str(e)}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Arguments to pass to the Python script.",
                ),
            ),
        },
    ),
)
