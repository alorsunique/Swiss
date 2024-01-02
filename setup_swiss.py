# Setup file for Swiss

import os
from pathlib import Path

# Create the resource path text file

resources_dir_text = "Resources_Path.txt"

with open(resources_dir_text, 'a') as writer:
    writer.close()

# Read the directory

entry_list = []

with open(resources_dir_text, 'r') as reader:
    entry_list.append(reader.read())
    reader.close()

# Create the necessary folders

if entry_list[0]:
    resources_dir = Path(entry_list[0])
    print(f"Resources Directory: {resources_dir}")

    if not resources_dir.exists():
        os.mkdir(resources_dir)

    input_dir = resources_dir / "Input"
    if not input_dir.exists():
        os.mkdir(input_dir)

    move_dir = resources_dir / "Move"
    if not move_dir.exists():
        os.mkdir(move_dir)

    rescale_dir = resources_dir / "Rescale"
    if not rescale_dir.exists():
        os.mkdir(rescale_dir)

    cropped_dir = resources_dir / "Cropped"
    if not cropped_dir.exists():
        os.mkdir(cropped_dir)

    trier_dir = resources_dir / "Sort"
    if not trier_dir.exists():
        os.mkdir(trier_dir)

    rescale_dir = rescale_dir / "Rescale"
    if not rescale_dir.exists():
        os.mkdir(rescale_dir)
