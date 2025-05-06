# This script should rename files based on their modification times

import os
import sys
from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))



with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

input_dir = resources_dir / "Input"


for entry in input_dir.iterdir():
    new_name = entry.stem.replace("Slide","")
    new_name_lead = new_name.zfill(4)
    print(new_name_lead)
    output_name = f"{new_name_lead}{entry.suffix}"
    print(output_name)

    output_path = input_dir / output_name

    os.rename(entry,output_path)
