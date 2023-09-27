# This script should rename the upscaled images in the Wallpaper Project

import os
from datetime import datetime
from pathlib import Path

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent

wallpaper_dir = upper_dir / "Wallpaper Project"
to_scale_dir = wallpaper_dir / "To Upscale"

dgb_dir = wallpaper_dir / "DGB Upscale"

to_scale_list = []

for file in to_scale_dir.iterdir():
    if file.stem not in to_scale_list:
        to_scale_list.append(file.stem)

dgb_list = []

for file in dgb_dir.iterdir():
    dgb_list.append(file)

for file in dgb_list:

    time_filter = datetime.now()
    time_filter = time_filter.strftime("%H%M%S")

    preliminary_name = f"{time_filter}_{file.name}"
    preliminary_path = dgb_dir / preliminary_name

    os.rename(file, preliminary_path)

    file_name = file.stem.replace("_", "-").upper()

    for entry in to_scale_list:

        entry_name = entry.replace("_", "-").upper()

        if entry_name in file_name:

            shorten_name = file_name[file_name.index(entry_name):file_name.index(entry_name) + len(entry_name) + 1]
            if shorten_name[-1] == "-":
                shorten_name = shorten_name[:-1]

            print(f"Concatenate Name: {shorten_name}")
            print(f"Entry Name: {entry_name}")

            if entry_name == shorten_name:
                file_handle = file.suffix
                new_name = f"{entry}{file_handle}"

                new_file_path = dgb_dir / new_name

                if new_file_path.exists():
                    same_file_count = 0
                    while True:
                        same_file_count += 1
                        same_new_name = f"{entry}_Duplicate_{same_file_count}{file_handle}"
                        same_dir = dgb_dir / same_new_name
                        if not same_dir.exists():
                            new_file_path = same_dir
                            break

                print(f"Preliminary: {preliminary_path}")
                print(f"New: {new_file_path}")
                os.rename(preliminary_path, new_file_path)

dgb_list.clear()

for file in dgb_dir.iterdir():
    dgb_list.append(file.stem)

set_to_scale = set(to_scale_list)
set_dgb = set(dgb_list)

difference = list(set_to_scale.difference(set_dgb))
print(difference)
