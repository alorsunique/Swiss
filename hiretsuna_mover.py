# Automatically moves output from Stable Diffusion


import os
import shutil
import sys
import time
from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

from Modules import modtime

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

hiretsuna_pointer_text = resources_dir / "hiretsuna_pointer.txt"

with open(hiretsuna_pointer_text, "r") as hiretsuna_pointer_lines:
    path_list = hiretsuna_pointer_lines.readlines()

creation_dir = Path(str(path_list[0]).replace('\n', '').replace('"', ''))
refine_dir = Path(str(path_list[2]).replace('\n', '').replace('"', ''))

output_dir = Path(str(path_list[1]).replace('\n', '').replace('"', ''))


def get_next_run_time(minute_root, interval_minute):
    current_time = time.time()

    # hour_mark = int(time.strftime("%H", time.localtime(current_time)))
    minute_mark = int(time.strftime("%M", time.localtime(current_time)))
    second_mark = int(time.strftime("%S", time.localtime(current_time)))

    minute_root = minute_root
    interval_minute = interval_minute

    next_minute = minute_root + ((((minute_mark - minute_root) // interval_minute) + 1) * interval_minute)

    if next_minute >= 60:
        # This resets it back to the hour
        next_run_time = current_time + ((60 - minute_mark) * 60 - second_mark)
    else:
        next_run_time = current_time + ((next_minute - minute_mark) * 60 - second_mark)

    return next_run_time


minute_root = 0
interval_minute = 3

sleep_second = get_next_run_time(minute_root, interval_minute) - time.time()
time.sleep(sleep_second)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

while True:

    for entry in output_dir.rglob('*'):
        if entry.is_file():
            source_file = entry
            shutil.move(source_file, creation_dir)

    modtime.preliminary_naming(creation_dir)

    indicator = ""
    if not indicator == "":
        indicator = f"{indicator}_"

    modtime.mod_renaming(creation_dir, indicator)

    modtime.preliminary_naming(refine_dir)

    indicator = "Refine"
    if not indicator == "":
        indicator = f"{indicator}_"

    modtime.mod_renaming(refine_dir, indicator)

    for entry in output_dir.iterdir():
        shutil.rmtree(entry)

    sleep_second = get_next_run_time(minute_root, interval_minute) - time.time()
    time.sleep(sleep_second)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
