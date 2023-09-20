# This project sorts images into respective quarters based on the modification date
# Use for images taken using phone

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
    print(mod_year)

    year_folder = os.path.join(quarter_dir, mod_year)
    if not os.path.exists(year_folder):
        os.mkdir(year_folder)

    print(mod_year)

    shutil.move(src_to_move, year_folder)
