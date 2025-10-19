import os
from google.genai import types

def write_file(working_directory, file_path, content):
    target_file = os.path.join(working_directory, file_path)

    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        error_msg = f'    Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        # print(error_msg)
        return error_msg


    try:
      # if the target_file doesn't exist, create it.
      if not os.path.exists(target_file):
          os.makedirs(os.path.dirname(target_file), exist_ok=True)
      # overwrite the contents of the target_file with contents

      with open(target_file, 'w') as file:
          file.write(content)
      success_msg = f'    Successfully wrote to "{target_file}" ({len(content)} characters written)'
      # print(success_msg)
      return success_msg
    except Exception as e:
      error_msg = f'    Error: Could not write to file "{target_file}". Exception: {str(e)}'
      # print(error_msg)
      return error_msg

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)