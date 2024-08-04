import os
import shutil
from pathlib import Path

source_dir = Path(str(input(f"Source Path: ")).replace('"', ''))
sink_dir = Path(str(input(f"Sink Path: ")).replace('"', ''))

count = 5
copy_confirmation = True
while count > 0:
    print(f"\nSource Directory: {source_dir}")
    print(f"Sink Directory: {sink_dir}\n")
    choice = str(input(f"Any other input will stop. Input Y to continue: ").lower())
    if choice != "y":
        copy_confirmation = False
        break
    count -= 1

if copy_confirmation:

    single_post_list = []
    multiple_post_list = []

    for entry in source_dir.rglob('*'):

        if entry.is_file() and entry.suffix == ".jpg":
            if entry.stem[-3:] == "UTC":
                single_post_list.append(entry)
            else:
                multiple_post_list.append(entry)

    deletable_list = []
    for file in multiple_post_list:
        if file.stem[-5:] != "UTC_1":
            deletable_list.append(file)

    single_set = set(single_post_list)
    multiple_set = set(multiple_post_list)
    deletable_set = set(deletable_list)

    append_set = multiple_set.difference(deletable_set)
    lead_list = sorted(single_set.union(append_set))

    for entry in lead_list:
        relative_path = entry.relative_to(source_dir)
        output_dir = sink_dir / relative_path.parent

        if not output_dir.exists():
            os.makedirs(output_dir)

        output_name = entry.name
        output_path = output_dir / output_name

        if not output_path.exists():
            print(f"{str(relative_path.parent).ljust(40)} | {str(entry.name).ljust(40)} | Copying")
            shutil.copy2(entry, output_path)

        else:
            print(f"{str(relative_path.parent).ljust(40)} | {str(entry.name).ljust(40)} | Already Copied")

else:
    print("Process stopped")
