import os
import sys
from pathlib import Path

from PIL import Image
from moviepy.editor import VideoFileClip

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

video_folder_dir = resources_dir / "Video"
workspace_dir = resources_dir / "Temporary Workspace"

os.chdir(workspace_dir)

input_dir = video_folder_dir / "Input"
output_dir = video_folder_dir / "Output"

file_list = []

for entry in input_dir.rglob('*'):
    if entry.is_file():
        file_list.append(entry)

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

            selected_file = file_list[choice - 1]

            output_folder_dir = output_dir / f"{selected_file.stem}"
            if not output_folder_dir.exists():
                os.mkdir(output_folder_dir)

            video = VideoFileClip(str(selected_file))
            fps = video.fps
            frames = video.iter_frames(fps=fps)
            duration = video.duration
            frame_estimate = int(duration * fps)

            new_frame_list = []
            frame_count = 0

            for frame in frames:
                frame_count += 1
                image = Image.fromarray(frame)
                output_name = f"{selected_file.stem}_Frame_{str(frame_count).zfill(6)}.jpg"
                output_path = output_folder_dir / output_name
                image.save(output_path, quality=100)

            video.close()

    except:
        print(f"Did not catch that")

    if break_condition:
        break

# Clearing of the temporary workspace
for file in workspace_dir.iterdir():
    print(f"Removing: {file.name}")
    os.remove(file)
