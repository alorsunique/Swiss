# Built for Nova2i crop
# Built for S20FE crop
# Crop dimensions found below

import os
import time

from PIL import Image

# Get the directory

project_dir = os.getcwd()
environment_dir = os.path.join(project_dir, "Environment")
crop_dir = os.path.join(project_dir, "Cropped")

if not os.path.exists(environment_dir):
    os.mkdir(environment_dir)

if not os.path.exists(crop_dir):
    os.mkdir(crop_dir)


crop_dict = dict()

huawei_crop = [0,1080,85,1975]
samsung_crop = [0,1080,135,2017]

crop_dict["Huawei"] = huawei_crop
crop_dict["Samsung"] = samsung_crop

# Select the source of dimension here

left, right, top, bottom = crop_dict["Samsung"]

# Begins the cropping and renaming process here.

count = 0

for to_crop in os.listdir(environment_dir):
    count += 1
    img_dir = os.path.join(environment_dir, to_crop)
    img_in = Image.open(img_dir)

    split_tup = os.path.splitext(img_dir)

    src_filehandle = os.path.join(environment_dir, img_dir)

    mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(img_dir)))

    # This segment cleans up the modified time into chunks
    mod_dt = mod_time.split(" ")
    mod_d = mod_dt[0].split(":")
    mod_t = mod_dt[1].split(":")
    chunk_d = ""
    chunk_t = ""
    for date_chunk in mod_d:
        chunk_d += date_chunk
    for time_chunk in mod_t:
        chunk_t += time_chunk

    timestamp = f"{chunk_d}_{chunk_t}{split_tup[1]}"

    filename = f"FromIGStory_{timestamp}"

    img_out = img_in.crop((left, top, right, bottom))
    img_out.save(os.path.join(crop_dir, filename), quality=100, subsampling=0)

    print(count)
