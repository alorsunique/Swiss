# This script should rename files based on their modification times

import os
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageOps

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))


dimension_dir = resources_dir / "Dimension Pull"

if not dimension_dir.exists():
    os.mkdir(dimension_dir)




search_input = Path(str(input(f"Input Path: ")).replace('"', ''))

print(search_input)

print(search_input.name)

parent_dir = dimension_dir / search_input.name

width = 1440
height = 1800




def add_replica_mod_time(replica_mod_date_dict, image_file):
    replica_mod_time = os.path.getmtime(image_file)
    replica_mod_date_dict[image_file] = replica_mod_time
    return replica_mod_date_dict




image_compare_dir = resources_dir / "Image Compare"
replica_dir = image_compare_dir / "Replica"


replica_mod_date_dict = dict()

for file in replica_dir.iterdir():
    replica_mod_date_dict = add_replica_mod_time(replica_mod_date_dict, file)

print(max(replica_mod_date_dict, key=replica_mod_date_dict.get))
print(max(replica_mod_date_dict.values()))
max_mod_date = max(replica_mod_date_dict.values())







if not parent_dir.exists():
    os.mkdir(parent_dir)

def get_shape(image_file):
    image = Image.open(image_file)
    return (image.size[0], image.size[1])

for file in search_input.rglob('*.jpg'):

    print(file)

    source_mod_time = os.path.getmtime(file)
    if not source_mod_time > max_mod_date:
        returned_width, returned_height = get_shape(file)
        print(f"Width: {returned_width} | Height: {returned_height}")
        if returned_width == width and returned_height == height:
            copy_dir = parent_dir / file.relative_to(search_input).parent
            print(f"copy dir: {copy_dir}")
            if not copy_dir.exists():
                os.makedirs(copy_dir)
            shutil.copy2(file, copy_dir)

for file in search_input.rglob('*.webp'):
    print(file)
    source_mod_time = os.path.getmtime(file)
    if not source_mod_time > max_mod_date:
        returned_width, returned_height = get_shape(file)
        print(f"Width: {returned_width} | Height: {returned_height}")
        if returned_width == width and returned_height == height:
            copy_dir = parent_dir / file.relative_to(search_input).parent
            print(f"copy dir: {copy_dir}")
            if not copy_dir.exists():
                os.makedirs(copy_dir)
            shutil.copy2(file, copy_dir)

for file in search_input.rglob('*.png'):
    print(file)
    source_mod_time = os.path.getmtime(file)
    if not source_mod_time > max_mod_date:
        returned_width, returned_height = get_shape(file)
        print(f"Width: {returned_width} | Height: {returned_height}")
        if returned_width == width and returned_height == height:
            copy_dir = parent_dir / file.relative_to(search_input).parent
            print(f"copy dir: {copy_dir}")
            if not copy_dir.exists():
                os.makedirs(copy_dir)
            shutil.copy2(file, copy_dir)


