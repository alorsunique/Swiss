# This script is meant to be called by story_call


def main():
    import os
    import shutil
    import time
    import sys
    from datetime import datetime
    from pathlib import Path

    from exif import Image

    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)
    sys.path.append(str(project_dir))

    from Modules import modtime

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    between_dir = resources_dir / "Between"

    for image_file in between_dir.iterdir():
        print(f"Working on: {image_file.name}")

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

    indicator = "Geschichte_"

    modtime.prelim_naming(between_dir)
    modtime.mod_renaming(between_dir, indicator)

    cropped = resources_dir / "Cropped"

    for file in between_dir.iterdir():
        if file.name not in os.listdir(cropped):
            shutil.move(file, cropped)

    shutil.rmtree(between_dir)
