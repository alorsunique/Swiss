# This script should rename files based on their modification times

import os
import sys
from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

from Modules import modtime
from Modules import mover

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

input_dir = resources_dir / "Input"
move_dir = resources_dir / "Move"

# Applies the preliminary rename

modtime.preliminary_naming(input_dir)

# Performs the final rename to the content

indicator = str(input(f"Input your desired indicator: "))
if not indicator == "":
    indicator = f"{indicator}_"

modtime.mod_renaming(input_dir, indicator)

# Checks the user if the content should be sorted by file extension

while True:
    move_condition = str(input(f"Sort the files by extensions? Y/N: "))
    move_condition = move_condition.upper()
    if move_condition == "Y":
        mover.mover(input_dir, move_dir, indicator)
        break
    elif move_condition == "N":
        print(f"Files are not moved")
        break
    else:
        print(f"Sorry did not catch that")
