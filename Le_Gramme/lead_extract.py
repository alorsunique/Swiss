import os
import shutil
import time
from pathlib import Path

from PIL import Image

project_dir = Path.cwd().parent
os.chdir(project_dir)


source_dir = Path(str(input(f"Path: ")).replace('"', ''))
sink_dir = Path(str(input(f"Path: ")).replace('"', ''))

single_post_list = []
multi_post_list = []



for entry in source_dir.rglob('*'):

    if entry.is_file() and entry.suffix == ".jpg":
        if entry.stem[-3:] == "UTC":
            single_post_list.append(entry)
        else:
            multi_post_list.append(entry)


deletable_list = []
for file in multi_post_list:
    if file.stem[-5:] != "UTC_1":
        deletable_list.append(file)


single_set = set(single_post_list)
multi_set = set(multi_post_list)
delete_set = set(deletable_list)

append_set = multi_set.difference(delete_set)

lead_set = single_set.union(append_set)

lead_list = sorted(lead_set)




for entry in lead_list:
    relative_path = entry.relative_to(source_dir)

    output_name = entry.name
    output_dir = sink_dir / relative_path.parent

    if not output_dir.exists():
        os.makedirs(output_dir)

    output_path = output_dir/output_name

    if not output_path.exists():
        print(f"{relative_path} | {entry.name} copied")
        shutil.copy2(entry,output_path)

    else:
        print(f"{relative_path} | {entry.name} already copied")

