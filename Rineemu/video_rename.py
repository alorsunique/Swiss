# Renames video downloaded using downloaders like JDownloader 2
# Can be used to remove the resolution in the file name
# Example (1920 x 1080)

import os
from pathlib import Path

project_dir = Path.cwd().parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

input_dir = resources_dir / "Input"

# Run through removes the ending part of the string where the resolution of the
# downloaded file is stated. Example (1920 x 1080)

run_condition = input(f"Select Y to perform a run through: ").upper()

if run_condition == "Y":

    for file in input_dir.iterdir():
        src_file = file

        title_string = file.stem
        file_handle = file.suffix

        # Search for the last parenthesis in the title. This is the closing parenthesis

        countdown = len(title_string)
        while True:
            countdown -= 1
            if title_string[countdown] == "(":
                break

        title_string = title_string[:countdown - 1]

        new_filename_string = title_string + file_handle
        new_filename_dir = input_dir / new_filename_string
        os.rename(src_file, new_filename_dir)

for file in input_dir.iterdir():
    print(f"Run Through Results: {file.name}")

# Remove strings located at the first and last sections of the file name

front_string_remove = input(f'Front String: ')
back_string_remove = input(f'Back String: ')

for file in input_dir.iterdir():
    print(f"Initial: {file.name}")

    src_file = file

    title_string = file.stem
    file_handle = file.suffix

    title_string = title_string.replace(front_string_remove, '')
    title_string = title_string.replace(back_string_remove, '')
    title_string = title_string.strip()

    new_filename_string = title_string + file_handle
    print(f"Final: {new_filename_string}")

    new_filename_dir = input_dir / new_filename_string

    os.rename(src_file, new_filename_dir)
