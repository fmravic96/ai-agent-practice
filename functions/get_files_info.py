import os


def format_file_info(file_name, file_path):
    file_size = os.path.getsize(file_path)
    is_dir = os.path.isdir(file_path)
    return f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"


def get_files_info(working_directory, directory="."):

    full_path_dir = os.path.abspath(os.path.join(working_directory, directory))
    # Ensure the resolved path is within the working directory
    if not full_path_dir.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path_dir):
        return f'Error: "{directory}" is not a directory'

    return "\n".join(
        [
            format_file_info(f, os.path.join(full_path_dir, f))
            for f in os.listdir(full_path_dir)
        ]
    )
