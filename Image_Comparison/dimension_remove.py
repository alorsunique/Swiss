# This script should rename files based on their modification times

import os
import shutil
import sys
from pathlib import Path
from PIL import Image, ImageOps

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))


dimension_dir = resources_dir / "Dimension Pull"

if not dimension_dir.exists():
    os.mkdir(dimension_dir)



def add_replica_mod_time(replica_mod_date_dict, image_file):
    replica_mod_time = os.path.getmtime(image_file)
    replica_mod_date_dict[image_file] = replica_mod_time
    return replica_mod_date_dict


image_compare_dir = resources_dir / "Image Compare"
replica_dir = image_compare_dir / "Replica"


replica_mod_date_dict = dict()

for file in replica_dir.iterdir():
    replica_mod_date_dict = add_replica_mod_time(replica_mod_date_dict, file)

print(max(replica_mod_date_dict, key=replica_mod_date_dict.get))
print(max(replica_mod_date_dict.values()))
max_mod_date = max(replica_mod_date_dict.values())

print(max_mod_date)

for entry in dimension_dir.rglob('*'):
    if entry.is_file():
        source_mod_time = os.path.getmtime(entry)
        if source_mod_time > max_mod_date:
            print(entry)
            os.remove(entry)


