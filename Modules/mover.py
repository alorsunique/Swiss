# This essentially moves stuff based on the filename and their extensions
# This is a package

import os
import shutil


def mover(src_dir, dst_dir, in_indicator):
    environment_dir = src_dir  # Source directory
    indicator = in_indicator
    move_dir = dst_dir  # Sink directory
    for file in os.listdir(environment_dir):
        filename_tup = os.path.splitext(file)
        folder_ext = filename_tup[1].split(".")

        # Prepares the subfolders
        drop_folder = os.path.join(move_dir, indicator + folder_ext[1])
        if not os.path.exists(drop_folder):
            os.mkdir(drop_folder)

        src_dir = os.path.join(environment_dir, file)

        shutil.move(src_dir, drop_folder)
