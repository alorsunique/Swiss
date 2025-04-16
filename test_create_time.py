# This script should rename files based on their modification times

import os
import sys
import time
from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

input_dir = resources_dir / "Input"

for file in input_dir.iterdir():
    print(file)
    print(f"Mod: {os.path.getmtime(file)}")
    print(type(os.path.getmtime(file)))

    formatted_mod_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(file)))

    print(formatted_mod_time)

    print(f"Create: {os.path.getctime(file)}")
    print(type(os.path.getctime(file)))

    formatted_mod_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(file)))

    print(formatted_mod_time)