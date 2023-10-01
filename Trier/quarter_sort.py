# This project sorts images into respective quarters based on the modification date

import os
import shutil
import time

from pathlib import Path

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
resources_dir = upper_dir / "PycharmProjects Resources" / "Swiss Resources"

input_dir = resources_dir / "Input"
trier_dir = resources_dir / "Sort"

if not trier_dir.exists():
    os.mkdir(trier_dir)

while True:  # Checks for the quarter condition
    quarter_condition = str(input(f"Sort by quarter. Y/N: ")).upper()
    if quarter_condition == "Y" or quarter_condition == "N":
        break
    else:
        print(f"Sorry did not catch that")

for file in input_dir.iterdir():

    src_to_move = file
    mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(src_to_move)))
    print(mod_time)

    datetime_chunk = mod_time.split(" ")
    date_chunk = datetime_chunk[0].split(":")

    mod_year = date_chunk[0]
    mod_month = int(date_chunk[1].lstrip("0"))
    mod_day = int(date_chunk[2].lstrip("0"))
    print(mod_year)
    print(str(mod_month))
    print(str(mod_day))

    year_folder = trier_dir / mod_year

    if not year_folder.exists():
        os.mkdir(year_folder)

    move_folder = year_folder

    if quarter_condition == "Y":
        print("IN")
        # Condition for determining the quarter

        if mod_month < 4:
            quarter = "Q1"
        elif mod_month == 4:
            if mod_day == 1:
                quarter = "Q1"
            else:
                quarter = "Q2"
        elif 4 < mod_month < 7:
            quarter = "Q2"
        elif mod_month == 7:
            if mod_day == 1:
                quarter = "Q2"
            else:
                quarter = "Q3"
        elif 7 < mod_month < 10:
            quarter = "Q3"
        elif mod_month == 10:
            if mod_day == 1:
                quarter = "Q3"
            else:
                quarter = "Q4"
        else:
            quarter = "Q4"

        quarter_folder = year_folder / f"{mod_year}{quarter}"
        print(quarter_folder)
        if not quarter_folder.exists():
            os.mkdir(quarter_folder)

        move_folder = quarter_folder

    shutil.move(src_to_move, move_folder)
