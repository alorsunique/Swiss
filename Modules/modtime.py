# This takes in the date modified of the file renames it
# This is a package

import os
import time
from datetime import datetime


# This preliminary naming is to ensure no same name will be handled in the process
def prelim_naming(dir_parameter):
    file_count = 0
    environment_dir = dir_parameter
    for file in os.listdir(environment_dir):
        file_count += 1
        # filename_tup is a tuple. [1] returns file extension
        filename_tup = os.path.splitext(file)

        # time_filter serves to add randomness
        time_filter = datetime.now()
        time_filter = time_filter.strftime("%H%M%S")

        # This is the after name of the file
        prelim_name = os.path.join(environment_dir, f"{file_count}_{time_filter}{filename_tup[1]}")

        # This takes the directory of the current file handled
        src_file = os.path.join(environment_dir, file)

        os.rename(src_file, prelim_name)


def mod_renaming(dir_parameter, in_indicator):
    file_count = 0
    environment_dir = dir_parameter
    indicator = in_indicator
    for file in os.listdir(environment_dir):
        print(file)
        file_count += 1
        filename_tup = os.path.splitext(file)

        src_file = os.path.join(environment_dir, file)

        # Gets the modification time as specified in the properties of the file
        mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(src_file)))

        # This segment cleans up the modified time. Joins the date as one string and the time as another string
        mod_dt = mod_time.split(" ")
        mod_d = mod_dt[0].split(":")
        mod_t = mod_dt[1].split(":")
        chunk_d = ""
        chunk_t = ""
        for date_split in mod_d:
            chunk_d += date_split
        for time_split in mod_t:
            chunk_t += time_split

        new_file_name = f"{indicator}{chunk_d}_{chunk_t}{filename_tup[1]}"
        new_file_name = os.path.join(environment_dir, new_file_name)

        if os.path.exists(new_file_name):
            same_file_count = 0
            while True:
                same_file_count += 1

                new_file_name = f"{indicator}{chunk_d}_{chunk_t}_{same_file_count}{filename_tup[1]}"
                new_file_name = os.path.join(environment_dir, new_file_name)
                if not os.path.exists(new_file_name):
                    break
        os.rename(src_file, new_file_name)

    print(f"Files modified: {file_count}")
