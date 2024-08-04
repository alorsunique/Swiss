import os
from pathlib import Path

from PIL import Image


def tree_resize_image(input_dir, rescale_dir, minimum_size):
    min_size = minimum_size
    image_list = []
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    for entry in input_dir.rglob('*'):
        if entry.is_file and str(entry).endswith(image_extensions):
            image_list.append(entry)

    for entry in image_list:
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

        print(f"{entry.name} | {(horizontal_size, vertical_size)} | {(new_horizontal, new_vertical)}")

        relative_dir = entry.relative_to(input_dir).parent
        output_dir = rescale_dir / relative_dir

        if not output_dir.exists():
            os.makedirs(output_dir)

        output_path = output_dir / entry.name
        rescaled_image = working_image.resize((new_horizontal, new_vertical), Image.LANCZOS)
        rescaled_image.save(str(output_path))

        rescaled_image.close()
        working_image.close()

        mod_time = os.path.getmtime(entry)
        os.utime(output_path, (mod_time, mod_time))


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    input_dir = resources_dir / "Input"
    rescale_dir = resources_dir / "Rescale"

    minimum_size = 1080

    tree_resize_image(input_dir, rescale_dir, minimum_size)
