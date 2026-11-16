
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path



def reverse_name(compressed_string):

    compressed_string_split = compressed_string.split("_")

    uncompressed_day = f"{compressed_string_split[0][:4]}-{compressed_string_split[0][4:6]}-{compressed_string_split[0][6:]}"

    uncompressed_time = f"{compressed_string_split[1][:2]}-{compressed_string_split[1][2:4]}-{compressed_string_split[1][4:]}"

    if len(compressed_string_split) > 2:
        uncompressed_string = f"{uncompressed_day}_{uncompressed_time}_UTC_{compressed_string_split[2]}"
    else:
        uncompressed_string = f"{uncompressed_day}_{uncompressed_time}_UTC"

    return uncompressed_string


def main():
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent

    # Change working directory to project directory
    os.chdir(project_dir)
    sys.path.append(str(project_dir))

    # Takes note of starting time
    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Session Start Time: {current_time}")

    with open("Resources_Path.txt", "r") as read_text:
        lines = read_text.readlines()

    resources_dir = Path(lines[0].replace('"', ''))

    otter_image_pull_dir =  resources_dir / "Otter Image Pull"

    if not otter_image_pull_dir.exists():
        os.mkdir(otter_image_pull_dir)

    otter_image_pull_text = resources_dir / "Otter_Image_Pull.txt"

    with open(otter_image_pull_text, "r") as read_text:
        lines = read_text.readlines()

    image_pull_list = []

    for entry in lines:
        image_pull_list.append(entry.strip())

    otter_dir = Path("E:\Projects\Otter")

    for category in otter_dir.iterdir():

        for account in category.iterdir():

            for entry in image_pull_list:

                formatted_entry = reverse_name(entry)

                check_path = account / f"{formatted_entry}.jpg"
                #print(check_path)

                if check_path.exists():

                    copy_folder = otter_image_pull_dir / account.name

                    if not copy_folder.exists():
                        os.mkdir(copy_folder)

                    copy_path = copy_folder / f"{formatted_entry}.jpg"
                    shutil.copy2(check_path, copy_path)

                else:
                    print(f"{check_path} | Image not found")



if __name__ == "__main__":
    main()