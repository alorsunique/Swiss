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

session_folder_list = []

for session_folder in screenshot_dir.iterdir():
    if session_folder.is_dir():
        session_folder_list.append(session_folder)

count = 0
for entry in session_folder_list:
    print(f"{count + 1}. {entry.name}")
    count += 1

break_condition = False

while True:
    session_input = input(f"Session: ")
    try:
        session_choice = int(session_input) - 1

        if session_choice >= 0 and session_choice < len(session_folder_list):

            print(f"Loading frames")

            frame_list = []
            for screenshot in session_folder_list[session_choice].iterdir():
                frame = Image.open(screenshot)
                frame_list.append(np.array(frame))

            clip = ImageSequenceClip(frame_list, fps=12)

            output_path = screenshot_compile_dir / f"{session_folder_list[session_choice].name}_Compile.mp4"
            clip.write_videofile(str(output_path), codec='libx264')

            break_condition = True

        else:
            print(f"Out of Bounds")

    except:
        print(f"Invalid Input")

    if break_condition:
        break
