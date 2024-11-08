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

current_time = time.time()
sleep_second = 60 - (current_time % 60)

time.sleep(sleep_second)

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

    current_time = time.time()
    sleep_second = 60 - (current_time % 60)
    time.sleep(sleep_second)
    time.sleep(180)
