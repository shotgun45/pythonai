import os

def write_file(working_directory, file_path, content):
    try:
        # Construct absolute paths
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        base_path = os.path.abspath(working_directory)

        # Check path restriction
        if not full_path.startswith(base_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure parent directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Write content to file (overwrite)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"
