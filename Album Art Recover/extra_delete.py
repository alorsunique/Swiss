import os
from pathlib import Path

era_folder = Path(str(input(f"Path: ")).replace('"', ''))

# Removes JSON txt and mp4


for file in era_folder.iterdir():
    if file.suffix != ".jpg":
        os.remove(file)

# Takes note of single image posts and multi images posts

single_post_list = []
multi_post_list = []

for file in era_folder.iterdir():
    if file.stem[-3:] == "UTC":
        single_post_list.append(file)
    else:
        multi_post_list.append(file)

# Tracks all not first images

deletable_list = []

for file in multi_post_list:
    if file.stem[-5:] != "UTC_1":
        deletable_list.append(file)

print(f"Deletable: {deletable_list}")

# Deletes all deletables

for file in deletable_list:
    os.remove(file)
