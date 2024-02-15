import os
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

# Perform preliminary rename here

file_list = []

for image_file in input_dir.iterdir():
    file_list.append(image_file)

image_amount = len(file_list)
count = 0
for entry in file_list:
    new_name = f"{str(image_amount-count).zfill(4)}.jpg"
    count += 1
    new_path = input_dir / new_name
    os.rename(entry,new_path)

file_list = []
width_list = []
height_list = []

for image_file in input_dir.iterdir():
    file_list.append(image_file)
    current_image = Image.open(image_file)
    width, height = current_image.size
    width_list.append(width)
    height_list.append(height)

print(f"Width: {width_list}")
print(f"Height: {height_list}")

max_width = max(width_list)
max_height = max(height_list)

print(f"Max Width: {max_width} | Max Height: {max_height}")

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
        output_path = temporary_workspace_dir / f"Horizontal_{str(vertical_count).zfill(4)}.jpg"
        joined_image.save(output_path)

horizontal_file_list = []
horizontal_width_list = []
horizontal_height_list = []

for image_file in temporary_workspace_dir.iterdir():
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

current_time = time.strftime("%Y%m%d_%H%M%S")
output_path = stitch_dir / f"Stitch_{current_time}.jpg"
joined_image.save(output_path)

for file in horizontal_file_list:
    os.remove(file)

for file in file_list:
    os.remove(file)