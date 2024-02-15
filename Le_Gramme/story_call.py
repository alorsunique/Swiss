# Script to run for cropping stories

import os
import sys
from pathlib import Path

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

from Le_Gramme import story_crop
from Rineemu import story_rename

story_crop.main()
story_rename.main()