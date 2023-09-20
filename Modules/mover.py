# This essentially moves stuff based on the filename and their extensions
# This is a package

import os
import shutil
from pathlib import Path


def mover(src_dir, dst_dir, in_indicator):
    indicator = in_indicator

    input_dir = Path(src_dir)  # Source directory
    move_dir = Path(dst_dir)  # Sink directory
    for file in input_dir.iterdir():

        file_handle = file.suffix
        folder_ext = file_handle.split(".")

        # Prepares the subfolders
        drop_folder = move_dir / f"{indicator} {folder_ext[1]}"
        if not drop_folder.exists():
            os.mkdir(drop_folder)

        src_file = input_dir / file
        shutil.move(src_file, drop_folder)
