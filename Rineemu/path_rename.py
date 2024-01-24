# This script should take in a path and rename stuff there

import os
from pathlib import Path

# Ask for the target path
target_path = Path(input(f"Path: ").replace('"', ''))

if target_path.exists():

    # Takes note of all the files
    file_list = []
    for entry in target_path.rglob('*'):
        if entry.is_file():
            file_list.append(entry)

    # Takes note of initial substring and the final substring
    to_modify_string = str(input(f"String Input: "))
    modification_string = str(input(f"String Output: "))

    # Renames the files here
    for file in file_list:
        file_parent_dir = file.parent
        file_name = file.name

        new_file_name = file_name.replace(to_modify_string, modification_string)
        new_file_dir = file_parent_dir / new_file_name

        os.rename(file, new_file_dir)

else:
    print(f"Path does not exists")
