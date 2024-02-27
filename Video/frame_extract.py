import os
import sys
from pathlib import Path
from moviepy.editor import VideoFileClip
from PIL import Image

script_path = Path(__file__).resolve()
project_dir = script_path.parent.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

video_folder_dir = resources_dir / "Video"
workspace_dir = resources_dir / "Temporary Workspace"

output_dir = video_folder_dir / "Frame Extract"
if not output_dir.exists():
    os.mkdir(output_dir)


os.chdir(workspace_dir)

clip_output_dir = video_folder_dir / "Clip Output"



input_list = []

for entry in clip_output_dir.rglob('*'):
    if entry.is_file():
        input_list.append(entry)

break_condition = False
N = 8  # Padding

# Main loop of the program
while True:
    in_count = 0
    print(f"0: Exit Loop")
    for input_video in input_list:
        print(f"{in_count + 1}: {input_list[in_count].name}")
        in_count += 1

    try:
        choice = int(input(f"Select Option: "))

        if int(choice) == 0:
            break_condition = True
        elif int(choice) < 0 or int(choice) > len(input_list):
            print(f"Out of Bound")
        else:

            entry = input_list[choice - 1]

            output_folder_dir = output_dir / f"{entry.name}"
            if not output_folder_dir.exists():
                os.mkdir(output_folder_dir)

            print("HERE")


            clip = VideoFileClip(str(entry))

            fps = clip.fps
            frames = clip.iter_frames(fps=fps)
            duration = clip.duration
            frame_estimate = int(duration * fps)

            new_frame_list = []
            count = 0

            print("Here2")
            for frame in frames:
                count += 1
                print(type(frame))
                im = Image.fromarray(frame)
                output_name = f"{entry.name}_Frame_{count:0{8}}.jpg"
                output_path = output_folder_dir / output_name
                print(output_name)
                im.save(output_path,quality = 100)

            clip.close()



    except:
        print(f"Did not catch that")

    if break_condition:
        break

# Clearing of the temporary workspace
for entry in workspace_dir.iterdir():
    print(f"Removing: {entry.name}")
    os.remove(entry)
