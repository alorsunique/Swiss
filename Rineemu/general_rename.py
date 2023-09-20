# This script should rename files based on their modification times

import os
from pathlib import Path

from Modules import modtime
from Modules import mover

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Swiss Resources"

input_dir = resources_dir / "Input"
move_dir = resources_dir / "Move"

if not input_dir.exists():
    os.mkdir(input_dir)

if not move_dir.exists():
    os.mkdir(move_dir)

modtime.prelim_naming(input_dir)  # Applies the preliminary rename

indicator = str(input(f"Input your desired indicator: "))
if not indicator == "":
    indicator = f"{indicator}_"

modtime.mod_renaming(input_dir, indicator)  # Performs the final rename to the content

while True:  # Checks the user if the content should be sorted by file extension
    move_con = str(input(f"Sort the files by extensions? Y/N: "))
    move_con = move_con.upper()
    if move_con == "Y":
        mover.mover(input_dir, move_dir, indicator)
        break
    elif move_con == "N":
        print(f"Files are not moved")
        break
    else:
        print(f"Sorry did not catch that")
