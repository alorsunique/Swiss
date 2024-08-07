import os
from pathlib import Path

from PIL import Image

project_dir = Path.cwd().parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

rescale_dir = resources_dir / "Rescale"
source_dir = Path(str(input(f"Path: ")).replace('"', ''))

# Take note of all images in the path provided

image_list = []
for entry in source_dir.rglob('*'):

    try:
        with Image.open(entry) as opened_image:
            opened_image.verify()
            image_check = True
    except (IOError, SyntaxError):
        image_check = False

    if entry.is_file() and image_check:
        image_list.append(entry)


def square_crop(input_image):
    horizontal_size = input_image.size[0]
    vertical_size = input_image.size[1]

    if horizontal_size < vertical_size:
        square_ratio = vertical_size / horizontal_size
    else:
        square_ratio = horizontal_size / vertical_size

    if square_ratio > 1.01:

        if horizontal_size < vertical_size:
            square_size = horizontal_size

            top_pixel = (vertical_size - square_size) // 2
            bottom_pixel = top_pixel + square_size

            cropped_image = input_image.crop((0, top_pixel, horizontal_size, bottom_pixel))

        else:
            square_size = vertical_size

            left_pixel = (horizontal_size - square_size) // 2
            right_pixel = left_pixel + square_size

            cropped_image = input_image.crop((left_pixel, 0, right_pixel, vertical_size))

        return cropped_image

    else:
        return None


for image in image_list:
    working_image = Image.open(image)

    cropped_image = square_crop(working_image)

    print(type(cropped_image))

    if not cropped_image == None:

        relative_path = image.relative_to(source_dir)

        output_name = image.name
        output_dir = rescale_dir / relative_path.parent / "Cropped"

        if not output_dir.exists():
            os.makedirs(output_dir)

        output_path = output_dir / output_name

        cropped_image.save(output_path)

    working_image.close()
