# Convert JFIF and WEBP to JPEG
# Metadata is messed up. Still needs work

import os
import time

from PIL import Image

# Get the directory

project_dir = os.getcwd()
environment_dir = os.path.join(project_dir, "Environment")
convert_dir = os.path.join(project_dir, "Converted")

if not os.path.exists(environment_dir):
    os.mkdir(environment_dir)

if not os.path.exists(convert_dir):
    os.mkdir(convert_dir)

count = 0

indicator = str(input("Input your desired indicator: "))

for to_rename in os.listdir(environment_dir):
    count += 1
    img_dir = os.path.join(environment_dir, to_rename)
    imgIn = Image.open(img_dir)

    split_tup = os.path.splitext(img_dir)

    src_filehandle = os.path.join(environment_dir, img_dir)

    mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(img_dir)))

    # This segment cleans up the modified time into chunks
    dt = mod_time.split(" ")
    d = dt[0].split(":")
    t = dt[1].split(":")
    c_date = ""
    c_time = ""
    for dateChunk in d:
        c_date += dateChunk
    for timeChunk in t:
        c_time += timeChunk

    timestamp = indicator + "_" + c_date + "_" + c_time + ".jpg"

    imgIn.save(os.path.join(convert_dir, timestamp), quality=95, subsampling=0)

    print(count)
