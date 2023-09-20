# Unfinished Project meant to add EXIF data

import os
import time

import piexif as piexif

cur_dir = os.getcwd()
environment_dir = os.path.join(cur_dir, "Environment")

for to_add in os.listdir(environment_dir):
    dict = piexif.load(os.path.join(environment_dir, to_add))

    exif_ifd = {piexif.ExifIFD.DateTimeOriginal: time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(
        os.path.getmtime(os.path.join(environment_dir, to_add)))), }
    exif_add = piexif.dump(exif_ifd)

    piexif.insert(exif_add, os.path.join(environment_dir, to_add))
