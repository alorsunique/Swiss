# This essentially moves stuff based on the filename and their extensions
# This is a package

import os
import shutil
from pathlib import Path


def mover(source_dir, destination_dir, in_indicator):
    indicator = in_indicator

    input_dir = Path(source_dir)
    move_dir = Path(destination_dir)

    for file in input_dir.iterdir():

        file_handle = file.suffix
        folder_extension = file_handle.split(".")

        # Prepares the subfolders
        drop_folder = move_dir / f"{indicator}{folder_extension[1]}"
        if not drop_folder.exists():
            os.mkdir(drop_folder)

        source_file = input_dir / file
        shutil.move(source_file, drop_folder)
