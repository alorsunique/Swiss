# This script is meant to be called by story_call

# Built for Nova2i crop
# Built for S20FE crop
# Crop dimensions found below




def main():
    import os
    import sys
    import time
    from pathlib import Path

    from PIL import Image

    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent
    os.chdir(project_dir)
    sys.path.append(str(project_dir))

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    input_dir = resources_dir / "Input"
    between_dir = resources_dir / "Between"
    if not between_dir.exists():
        os.mkdir(between_dir)

    crop_dict = dict()

    huawei_crop = [0, 1080, 85, 1975]
    samsung_crop = [0, 1080, 135, 2017]

    crop_dict["Huawei"] = huawei_crop
    crop_dict["Samsung"] = samsung_crop

    # Select the source of dimension here

    while True:
        crop_source = str(input(f"Select Crop Source: "))
        if crop_source == "Huawei" or crop_source == "Samsung":
            break
        else:
            print(f"Did not catch that")

    left, right, top, bottom = crop_dict[crop_source]

    # Begins the cropping and renaming process here.

    count = 0

    for file in input_dir.iterdir():
        count += 1

        file_handle = file.suffix

        src_filehandle = file
        mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(file)))

        # This segment cleans up the modified time into chunks

        datetime_chunk = mod_time.split(" ")
        date_chunk = datetime_chunk[0].split(":")
        time_chunk = datetime_chunk[1].split(":")
        rename_date = ""
        rename_time = ""
        for chunk in date_chunk:
            rename_date += chunk
        for chunk in time_chunk:
            rename_time += chunk

        timestamp = f"{rename_date}_{rename_time}{file_handle}"

        img_in = Image.open(file)
        img_out = img_in.crop((left, top, right, bottom))
        img_out_dir = between_dir / f"Between_{timestamp}"
        img_out.save(img_out_dir, quality=100, subsampling=0)

        print(f"Current Count: {count}")
