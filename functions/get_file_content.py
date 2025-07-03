import os

def get_file_content(working_directory, file_path):
    try:
        # Construct absolute paths
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        base_path = os.path.abspath(working_directory)

        # Restrict access to within the working directory
        if not full_path.startswith(base_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check that it's a file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file content
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Truncate if over 10,000 characters
        if len(content) > 10000:
            content = content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
