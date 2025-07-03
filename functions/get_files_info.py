import os

def get_files_info(working_directory, directory=None):
    try:
        # Default to "." if directory is None
        directory = directory or "."

        # Construct the absolute path
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        base_path = os.path.abspath(working_directory)

        # Check if the path is within the working directory
        if not full_path.startswith(base_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the path is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # Build and return string describing contents
        result_lines = []
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            try:
                file_size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                result_lines.append(
                    f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}"
                )
            except Exception as e:
                return f"Error: {str(e)}"

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"
