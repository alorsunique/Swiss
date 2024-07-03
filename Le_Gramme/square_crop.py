import os
import time
from pathlib import Path

from PIL import Image

project_dir = Path.cwd().parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

input_dir = resources_dir / "Input"
rescale_dir = resources_dir / "Rescale"

for file in input_dir.iterdir():
    print(file)

    working_image = Image.open(file)

    horizontal_size = working_image.size[0]
    vertical_size = working_image.size[1]

    print(horizontal_size)
    print(vertical_size)

    if horizontal_size < vertical_size:
        square_size = horizontal_size

        top_pixel = (vertical_size - square_size) // 2
        bottom_pixel = top_pixel + square_size

        cropped_image = working_image.crop((0, top_pixel, horizontal_size, bottom_pixel))

    else:
        square_size = vertical_size

        left_pixel = (horizontal_size - square_size) // 2
        right_pixel = left_pixel + square_size

        cropped_image = working_image.crop((left_pixel, 0, right_pixel, vertical_size))

    output_name = file.name
    output_path = rescale_dir / output_name

    cropped_image.save(output_path)

    working_image.close()