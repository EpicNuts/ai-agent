import os

def get_files_info(working_directory, directory="."):
    print(f"Result for '{directory}' directory:")
    target_directory = os.path.join(working_directory, directory)
 
    if not os.path.abspath(target_directory).startswith(os.path.abspath(working_directory)):
        print(f'    Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_directory):
        print(f'    Error: "{directory}" is not a directory')
        return f'    Error: "{directory}" is not a directory'

    files_info = []

    for item in os.listdir(target_directory):
        item_path = os.path.join(target_directory, item)
        file_size = os.path.getsize(item_path)
        is_dir = os.path.isdir(item_path)
        files_info.append(f' - {item}: file_size={file_size} bytes, is_dir={is_dir}')
    
    print("\n".join(files_info))
    return "\n".join(files_info)
