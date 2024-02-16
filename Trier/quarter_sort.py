# This project sorts images into respective quarters based on the modification date

import os
import shutil
import time

from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

input_dir = resources_dir / "Input"
trier_dir = resources_dir / "Sort"

while True:  # Checks for the quarter condition
    quarter_condition = str(input(f"Sort by quarter. Y/N: ")).upper()
    if quarter_condition == "Y" or quarter_condition == "N":
        break
    else:
        print(f"Sorry did not catch that")

for file in input_dir.iterdir():

    source_to_move = file
    mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(source_to_move)))
    print(f"Mod time: {mod_time}")

    datetime_chunk = mod_time.split(" ")
    date_chunk = datetime_chunk[0].split(":")

    mod_year = date_chunk[0]
    mod_month = int(date_chunk[1].lstrip("0"))
    mod_day = int(date_chunk[2].lstrip("0"))

    print(f"{mod_year} | {str(mod_month)} | {str(mod_day)}")

    year_folder = trier_dir / mod_year

    if not year_folder.exists():
        os.mkdir(year_folder)

    move_folder = year_folder

    if quarter_condition == "Y":
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
        print(f"Quarter: {quarter_folder.name}")
        if not quarter_folder.exists():
            os.mkdir(quarter_folder)

        move_folder = quarter_folder

    shutil.move(source_to_move, move_folder)
