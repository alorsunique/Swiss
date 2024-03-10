import os
from pathlib import Path

from PIL import Image

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

input_dir = resources_dir / "Input"

image_list = []

for entry in input_dir.rglob('*'):
    if entry.is_file():
        image_list.append(entry)

for entry in image_list:
    if entry.suffix == ".webp":
        image = Image.open(entry).convert("RGB")

        output_name = f"{entry.stem}.jpg"

        print(output_name)

        output_path = entry.parent / output_name

        print(output_path)

        image.save(output_path,"jpeg")
        image.close()