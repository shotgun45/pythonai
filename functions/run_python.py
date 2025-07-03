import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    try:
        # Construct absolute paths
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        base_path = os.path.abspath(working_directory)

        # Guard: file must be within working directory
        if not full_path.startswith(base_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Guard: file must exist
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'

        # Guard: must be a .py file
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute Python file with subprocess
        result = subprocess.run(
            ["python3", full_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory
        )

        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"

        if not output.strip():
            return "No output produced."

        return output.strip()

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run with Python.",
            ),
        },
    ),
)