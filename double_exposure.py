import itertools
import os
from pathlib import Path
import itertools
import numpy as np

from PIL import Image

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

double_exposure_dir = resources_dir / "Double Exposure"
double_in_dir = double_exposure_dir / "Input"
double_out_dir = double_exposure_dir / "Output"

image_input_list = []

for image_path in double_in_dir.iterdir():
    image_input_list.append(image_path)

image_pair_list = list(itertools.combinations(image_input_list,2))

print(image_pair_list)

first_ratio = 0.3

def channel_merge(first_image_channel, second_image_channel, first_ratio):
    first_array = np.array(first_image_channel)
    second_array = np.array(second_image_channel)

    first_array = first_array*first_ratio
    second_array = second_array*(1-first_ratio)

    merged_array = first_array + second_array

    merged_array = np.clip(merged_array,0, 255).astype(np.uint8)

    return merged_array

for pair in image_pair_list:
    first_image_path = pair[0]
    second_image_path = pair[1]

    first_image = Image.open(first_image_path)
    second_image = Image.open(second_image_path)

    first_image_size = first_image.size

    if not first_image_size == second_image.size:
        second_image = second_image.resize(first_image_size,Image.LANCZOS)

    first_red, first_green, first_blue = first_image.split()
    second_red, second_green, second_blue = second_image.split()

    merge_red = channel_merge(first_red,second_red,first_ratio)
    merge_green = channel_merge(first_green,second_green,first_ratio)
    merge_blue = channel_merge(first_blue,second_blue,first_ratio)

    red_channel = Image.fromarray(merge_red,mode="L")
    green_channel = Image.fromarray(merge_green, mode="L")
    blue_channel = Image.fromarray(merge_blue,mode="L")

    merge_image = Image.merge("RGB",(red_channel,green_channel,blue_channel))

    merge_image.show()

    first_image.close()
    second_image.close()
    merge_image.close()