# This project sorts images into respective quarters based on the modification date

import os
import shutil
import time

# Important packages

project_dir = os.getcwd()
environment_dir = os.path.join(project_dir, "Environment")
quarter_dir = os.path.join(project_dir, "Quarter")

if not os.path.exists(quarter_dir):
    os.mkdir(quarter_dir)

for to_move in os.listdir(environment_dir):
    src_to_move = os.path.join(environment_dir, to_move)
    mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(src_to_move)))
    print(mod_time)

    mod_dt = mod_time.split(" ")
    mod_d = mod_dt[0].split(":")

    mod_year = mod_d[0]
    mod_month = int(mod_d[1].lstrip("0"))
    mod_day = int(mod_d[2].lstrip("0"))
    print(mod_year)
    print(str(mod_month))
    print(str(mod_day))

    year_folder = os.path.join(quarter_dir, mod_year)
    if not os.path.exists(year_folder):
        os.mkdir(year_folder)

    quarter_folder = ""

    if mod_month < 4:
        quarter_folder = "Q1"
    elif mod_month == 4:
        if mod_day == 1:
            quarter_folder = "Q1"
        else:
            quarter_folder = "Q2"
    elif 4 < mod_month < 7:
        quarter_folder = "Q2"
    elif mod_month == 7:
        if mod_day == 1:
            quarter_folder = "Q2"
        else:
            quarter_folder = "Q3"
    elif 7 < mod_month < 10:
        quarter_folder = "Q3"
    elif mod_month == 10:
        if mod_day == 1:
            quarter_folder = "Q3"
        else:
            quarter_folder = "Q4"
    else:
        quarter_folder = "Q4"

    print(f"{mod_year} {str(mod_month)} {str(mod_day)}")
    print(quarter_folder)

    quarter_folder = os.path.join(year_folder, quarter_folder)
    print(quarter_folder)

    if not os.path.exists(quarter_folder):
        os.mkdir(quarter_folder)

    shutil.move(src_to_move, quarter_folder)
