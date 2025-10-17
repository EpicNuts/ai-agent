import os
from config import MAX_FILE_CONTENT_LENGTH

def get_file_content(working_directory, file_path):
    target_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        error_msg = f'    Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        print(error_msg)
        return error_msg
    
    if not os.path.isfile(target_file):
        error_msg = f'    Error: File is not found or is not a regular file: "{target_file}"'
        print(error_msg)
        return error_msg

    try:
        with open(target_file, 'r') as file:
            content = file.read()
            if len(content) > MAX_FILE_CONTENT_LENGTH:
                content = content[:MAX_FILE_CONTENT_LENGTH] + f'[...File "{target_file}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
            print(content)
            return content
    except Exception as e:
        error_msg = f'    Error: Could not read file "{target_file}". Exception: {str(e)}'
        print(error_msg)
        return error_msg