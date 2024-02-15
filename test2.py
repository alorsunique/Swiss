import os
import sys
from pathlib import Path

script_path = Path(__file__)

project_dir = script_path.parent
os.chdir(project_dir)

# sys.path.insert(0, str(project_dir/"Modules"))

module_dir = project_dir / "Modules"
os.chdir(module_dir)

print(Path.cwd())

import modtime

os.chdir(project_dir)


with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

input_dir = resources_dir / "Input"
move_dir = resources_dir / "Move"

modtime.prelim_naming(input_dir)  # Applies the preliminary rename
