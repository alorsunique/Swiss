import os
from pathlib import Path

from PIL import Image

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

double_exposure_dir = resources_dir / "Double Exposure"
double_in_dir = double_exposure_dir / "Input"
double_out_dir = double_exposure_dir / "Output"