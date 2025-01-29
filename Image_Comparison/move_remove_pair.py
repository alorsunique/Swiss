# This script should move the matches to another folder

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


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

    # Important directories
    image_compare_dir = resources_dir / "Image Compare"
    replica_dir = image_compare_dir / "Replica"
    source_dir = image_compare_dir / "Source"
    probable_dir = image_compare_dir / "Probable"

    move_set_dir = image_compare_dir / "Move Set"

    file_name_dict = dict()

    for entry in replica_dir.iterdir():
        file_name_dict[f"{entry.stem}"] = entry

    for group in probable_dir.iterdir():
        print(f"Current Group: {group}")
        replica_name = group.name

        group_folder_dir = move_set_dir / replica_name
        if not group_folder_dir.exists():
            os.mkdir(group_folder_dir)

        try:
            replica_original_path = file_name_dict[replica_name]
            print(f"Replica Original Path: {replica_original_path}")

            replica_destination_path = group_folder_dir / file_name_dict[replica_name].name
            print(f"Replica Destination Path: {replica_destination_path}")

            if replica_original_path.exists():
                shutil.move(replica_original_path, replica_destination_path)
        except:
            print("Replica does not exist")

        for entry in group.iterdir():
            print(f"Group Entry: {entry}")
            source_original_path = source_dir / entry.name

            print(f"Source Original Path: {source_original_path}")

            source_destination_path = group_folder_dir / entry.name

            print(f"Source Destination Path {source_destination_path}")
            if source_original_path.exists():
                shutil.move(source_original_path, source_destination_path)

    # Takes note of ending time
    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Session End Time: {current_time}")
    print(f"Total Session Run Time: {finish_time - start_time}")


if __name__ == "__main__":
    main()
