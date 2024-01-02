import os
from pathlib import Path

from PIL import Image

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Swiss Resources"

input_dir = resources_dir / "Input"
rescale_dir = resources_dir / "Rescale"

if not input_dir.exists():
    os.mkdir(input_dir)

if not rescale_dir.exists():
    os.mkdir(rescale_dir)

min_size = 1080

image_list = []

for entry in input_dir.rglob('*'):
    if entry.is_file():
        image_list.append(entry)

for entry in image_list:

    image_folder = entry.parent.name

    working_image = Image.open(entry)

    horizontal_size = working_image.size[0]
    vertical_size = working_image.size[1]

    min_pixel_size = min(working_image.size)

    if min_pixel_size > min_size:
        rescale_factor = min_pixel_size / min_size
        new_horizontal = int(horizontal_size / rescale_factor)
        new_vertical = int(vertical_size / rescale_factor)
    else:
        new_horizontal = horizontal_size
        new_vertical = vertical_size

    print(f"{entry.stem}{entry.suffix} | {(horizontal_size, vertical_size)} | {(new_horizontal, new_vertical)}")

    output_name = f"{entry.stem}_Rescaled{entry.suffix}"

    if image_folder != "Input":
        output_folder = rescale_dir / image_folder
        if not output_folder.exists():
            os.mkdir(output_folder)
    else:
        output_folder = rescale_dir

    output_path = output_folder / output_name
    rescaled_image = working_image.resize((new_horizontal, new_vertical), Image.LANCZOS)
    rescaled_image.save(str(output_path))

    rescaled_image.close()
    working_image.close()
