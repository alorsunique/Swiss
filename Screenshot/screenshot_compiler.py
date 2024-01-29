import os
from pathlib import Path

import numpy as np
from PIL import Image
from moviepy.editor import ImageSequenceClip

project_dir = Path.cwd().parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

screenshot_dir = resources_dir / "Screenshot"
screenshot_compile_dir = resources_dir / "Screenshot Compile"




frame_list = []

for screenshot in screenshot_dir.iterdir():
    frame = Image.open(screenshot)
    frame_list.append(np.array(frame))

clip = ImageSequenceClip(frame_list, fps=12)

output_path = screenshot_compile_dir / f"Screenshot Compile.mp4"
clip.write_videofile(str(output_path), codec='libx264')
