import os
import shutil
import time
from datetime import datetime
from pathlib import Path

from exif import Image

from Modules import modtime

# Get the directory

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Swiss Resources"

between_dir = resources_dir / "Between"

for image_file in between_dir.iterdir():
    print(image_file.name)

    image_handle = open(image_file, 'rb')
    image_object = Image(image_handle)
    image_handle.close()

    # In this part of the script, the date and time are extracted

    filename_split = image_file.stem.split("_")

    date_chunk = filename_split[1]
    time_chunk = filename_split[2]

    date_chunk = f"{date_chunk[:4]}:{date_chunk[4:6]}:{date_chunk[6:]}"
    time_chunk = f"{time_chunk[:2]}:{time_chunk[2:4]}:{time_chunk[4:]}"

    datetime_info = f"{date_chunk} {time_chunk}"
    datetime_object = datetime.strptime(datetime_info, '%Y:%m:%d %H:%M:%S')

    print(f"Date Time Info: {datetime_info} | Date Time Object: {datetime_object}")

    creation_time = time.mktime(datetime_object.timetuple())
    modification_time = time.mktime(datetime_object.timetuple())

    image_object["software"] = "Cropped Story"
    image_object["datetime_original"] = datetime_info
    image_object["datetime"] = datetime_info

    print(f"EXIF: {image_object.has_exif} | EXIF List: {image_object.list_all()}")

    crop_image_dir = between_dir / f"{image_file.name}"

    crop_handle = open(crop_image_dir, 'wb')
    crop_handle.write(image_object.get_file())
    crop_handle.close()

    os.utime(crop_image_dir, (creation_time, modification_time))

indicator = "From_Story_"

modtime.prelim_naming(between_dir)
modtime.mod_renaming(between_dir, indicator)

crop_dir = resources_dir / "Cropped"

for file in between_dir.iterdir():
    if file.name not in os.listdir(crop_dir):
        shutil.move(file, crop_dir)

shutil.rmtree(between_dir)
