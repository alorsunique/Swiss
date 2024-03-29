# This script should extract a subclip from a video file

import gc
import os
import sys
from pathlib import Path

from moviepy.editor import VideoFileClip

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

video_folder_dir = resources_dir / "Video"
workspace_dir = resources_dir / "Temporary Workspace"

# Changes the working directory to the workspace
os.chdir(workspace_dir)

input_dir = video_folder_dir / "Input"
if not input_dir.exists():
    os.mkdir(input_dir)

output_dir = video_folder_dir / "Output"
if not output_dir.exists():
    os.mkdir(output_dir)

file_list = []

for file in input_dir.rglob('*'):
    if file.is_file():
        file_list.append(file)

break_condition = False

# Main loop of the program
while True:
    count = 0
    print(f"0: Exit Loop")
    for input_video in file_list:
        print(f"{count + 1}: {file_list[count].name}")
        count += 1

    try:
        choice = int(input(f"Select Option: "))

        if int(choice) == 0:
            break_condition = True
        elif int(choice) < 0 or int(choice) > len(file_list):
            print(f"Out of Bound")
        else:
            # Creation of clips is done here

            selected_file = file_list[choice - 1]
            print(f"Video: {selected_file.stem}")
            t_i = int(input(f"Starting Time: "))
            t_f = int(input(f"Ending Time: "))

            output_name = f"{selected_file.stem}_{str(t_i).zfill(5)}-{str(t_f).zfill(5)}{selected_file.suffix}"
            output_path = output_dir / output_name

            video = VideoFileClip(str(selected_file))
            new_clip = video.subclip(t_i, t_f)
            new_clip.write_videofile(str(output_path), audio_codec='aac')
            new_clip.close()
            video.reader.close()
            gc.collect()

    except:
        print(f"Did not catch that")

    if break_condition:
        break

# Clearing of the temporary workspace
for file in workspace_dir.iterdir():
    print(f"Removing: {file.name}")
    os.remove(file)
