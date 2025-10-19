import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    target_file = os.path.join(working_directory, file_path)
    # print(target_file)

    if not os.path.abspath(target_file).startswith(os.path.abspath(working_directory)):
        error_msg = f'    Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
        # print(error_msg)
        return error_msg

    if not os.path.exists(target_file):
        error_msg = f'    Error: File "{file_path}" not found.'
        # print(error_msg)
        return error_msg

    if str(target_file).lower().endswith('.py') is False:
        error_msg = f'    Error: File "{file_path}" is not a Python file.'
        # print(error_msg)
        return error_msg

    try:
        completed_process = subprocess.run(
            ['python', file_path, *args],
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory
        )

        output = 'STDOUT: ' + completed_process.stdout
        error_output = 'STDERR: ' + completed_process.stderr

        if completed_process.returncode != 0:
            error_msg = f'    Error: Process exited with code {completed_process.returncode}. Stderr: {error_output}'
            # print(error_msg)
            return error_msg

        if not completed_process.stdout.strip() and not completed_process.stderr.strip():
            no_output_msg = '    No output produced by the script.'
            # print(no_output_msg)
            return no_output_msg

        print(output + error_output)
        return output + error_output

    except Exception as e:
        error_msg = f'    Error: executing Python file: {str(e)}'
        # print(error_msg)
        return error_msg

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file located within the working directory and returns its output.",
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
                ),
                description="A list of command line arguments to pass to the Python file.",
            ),
        },
    ),
)