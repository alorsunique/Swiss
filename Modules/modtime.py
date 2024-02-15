# This takes in the date modified of the file renames it

import os
import time
from datetime import datetime
from pathlib import Path


# This function is to ensure no same name will be handled in the process
def preliminary_naming(in_dir):
    file_count = 0
    input_dir = Path(in_dir)

    for file in input_dir.iterdir():
        file_count += 1

        file_handle = file.suffix

        # time_filter serves to add randomness
        time_filter = datetime.now()
        time_filter = time_filter.strftime("%H%M%S")

        # This is the after name of the file
        preliminary_name = input_dir / f"{str(file_count).zfill(8)}_{time_filter}{file_handle}"

        # This takes the directory of the current file handled
        src_file = input_dir / file

        os.rename(src_file, preliminary_name)


def mod_renaming(in_dir, in_indicator):
    file_count = 0
    input_dir = Path(in_dir)
    indicator = in_indicator
    for file in input_dir.iterdir():
        file_count += 1

        file_handle = file.suffix

        source_file = input_dir / file

        # Gets the modification time as specified in the properties of the file
        mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(source_file)))

        # This segment cleans up the modified time. Joins the date as one string and the time as another string

        datetime_chunk = mod_time.split(" ")
        date_chunk = datetime_chunk[0].split(":")
        time_chunk = datetime_chunk[1].split(":")
        rename_date = ""
        rename_time = ""
        for chunk in date_chunk:
            rename_date += chunk
        for chunk in time_chunk:
            rename_time += chunk

        new_file_name = f"{indicator}{rename_date}_{rename_time}{file_handle}"
        new_file_path = input_dir / new_file_name

        if new_file_path.exists():
            same_file_count = 0
            while True:
                same_file_count += 1
                name_split_tup = os.path.splitext(new_file_name)

                same_new_name = f"{name_split_tup[0]}_{same_file_count}{name_split_tup[1]}"
                same_path = input_dir / same_new_name
                if not same_path.exists():
                    new_file_path = same_path
                    break
        os.rename(source_file, new_file_path)

    print(f"Files modified: {file_count}")
