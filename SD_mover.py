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

sd_pointer_text = resources_dir / "sd_pointer.txt"

with open(sd_pointer_text, "r") as sd_pointer_lines:
    path_list = sd_pointer_lines.readlines()

creation_dir = Path(str(path_list[0]).replace('\n', '').replace('"', ''))
output_dir = Path(str(path_list[1]).replace('\n', '').replace('"', ''))


def get_next_run_time():
    """Calculate the next time to run the main function at the nearest 10-minute mark, including seconds."""
    current_time = time.time()
    # Get the current minutes and seconds
    minutes = int(time.strftime("%M", time.localtime(current_time)))
    seconds = int(time.strftime("%S", time.localtime(current_time)))

    # Calculate how many minutes to add to reach the next 10-minute mark
    next_minutes = ((minutes // 10) + 1) * 10
    if next_minutes == 60:  # Special case for the top of the hour
        next_run_time = current_time + ((60 - minutes) * 60 - seconds)
    else:
        next_run_time = current_time + ((next_minutes - minutes) * 60 - seconds)

    return next_run_time

sleep_second = get_next_run_time() - time.time()
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

    sleep_second = get_next_run_time() - time.time()
    time.sleep(sleep_second)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #current_time = time.time()
    #sleep_second = 60 - (current_time % 60)
    #time.sleep(sleep_second)
    #time.sleep(180)
