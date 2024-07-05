import os
import shutil
import time
from pathlib import Path

from PIL import Image

project_dir = Path.cwd().parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

input_dir = resources_dir / "Input"
stitch_dir = resources_dir / "Stitch"
temporary_workspace_dir = resources_dir / "Temporary Workspace"

# Make temporary copy of input

if temporary_workspace_dir.exists():
    shutil.rmtree(temporary_workspace_dir)
os.mkdir(temporary_workspace_dir)

temporary_input_dir = temporary_workspace_dir / "Input"
os.mkdir(temporary_input_dir)

for image_file in input_dir.iterdir():
    copy_path = temporary_input_dir / image_file.name
    shutil.copy2(image_file,copy_path)

# Perform preliminary rename on copied images here

file_list = []

for image_file in temporary_input_dir.iterdir():
    file_list.append(image_file)

image_amount = len(file_list)
count = 0
for entry in file_list:
    new_name = f"{str(image_amount-count).zfill(4)}.jpg"
    count += 1
    new_path = temporary_input_dir / new_name
    os.rename(entry,new_path)

# Take note of pixel and mod time information of the images

# New file list after renaming
file_list = []
width_list = []
height_list = []
mod_time_list = []

for image_file in temporary_input_dir.iterdir():

    mod_time_list.append(time.localtime(os.path.getmtime(image_file)))

    file_list.append(image_file)
    current_image = Image.open(image_file)
    width, height = current_image.size
    width_list.append(width)
    height_list.append(height)

earliest_time_instance = sorted(mod_time_list)[0]

print(f"Width: {width_list}")
print(f"Height: {height_list}")

temporary_horizontal_dir = temporary_workspace_dir / "Horizontal"
os.mkdir(temporary_horizontal_dir)

max_width = max(width_list)
max_height = max(height_list)

print(f"Max Width: {max_width} | Max Height: {max_height}")

# Create the horizontal slices

joined_image = Image.new("RGB", (max_width * 3, max_height))

count = 0
vertical_count = 0
total_width = 0

while count < len(file_list):
    current_image = Image.open(file_list[count])
    width = width_list[count]
    height = height_list[count]

    if width < max_width or height < max_height:
        print(f"Resizing")
        current_image = current_image.resize((max_width, max_height), Image.LANCZOS)

    total_width += max_width
    joined_image.paste(current_image, (total_width - max_width, 0))
    count += 1
    if count % 3 == 0:
        total_width = 0
        vertical_count += 1
        output_path = temporary_horizontal_dir / f"Horizontal_{str(vertical_count).zfill(4)}.jpg"
        joined_image.save(output_path)

horizontal_file_list = []
horizontal_width_list = []
horizontal_height_list = []

# Merge the horizontal images

for image_file in temporary_horizontal_dir.iterdir():
    horizontal_file_list.append(image_file)
    current_image = Image.open(image_file)
    width, height = current_image.size
    horizontal_width_list.append(width)
    horizontal_height_list.append(height)

print(f"Horizontal Width: {horizontal_width_list}")
print(f"Horiontal Height: {horizontal_height_list}")

max_width = max(horizontal_width_list)
max_height = max(horizontal_height_list)

print(f"Horizontal Max Width: {max_width} | Horizontal Max Height: {max_height}")

joined_image = Image.new("RGB", (max_width, max_height * len(horizontal_height_list)))

count = 0
total_height = 0
while count < len(horizontal_file_list):
    current_image = Image.open(horizontal_file_list[count])
    width = horizontal_width_list[count]
    height = horizontal_height_list[count]

    if width < max_width or height < max_height:
        print(f"Resizing")
        current_image = current_image.resize((max_width, max_height), Image.LANCZOS)

    total_height += max_height
    joined_image.paste(current_image, (0, total_height - max_height))
    count += 1

final_width, final_height = joined_image.size
print(f"Final Dimensions: ({final_width},{final_height})")

creation_time = time.mktime(earliest_time_instance)
modification_time = time.mktime(earliest_time_instance)

mod_time_string = time.strftime("%Y%m%d_%H%M%S",earliest_time_instance)

output_path = stitch_dir / f"Stitch_{mod_time_string}.jpg"
joined_image.save(output_path)

# Modify the modification time

os.utime(output_path, (creation_time, modification_time))

# Clean workspace

shutil.rmtree(temporary_workspace_dir)

for file in input_dir.iterdir():
    os.remove(file)