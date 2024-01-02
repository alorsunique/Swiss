from datetime import datetime
from pathlib import Path

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent

now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")


output_drive_dir = Path(f"{input('Drive Letter: ').upper()}:")
output_project = output_drive_dir/"Projects"
otter_dir = output_project / "Otter"

for division in otter_dir.iterdir():
    #print(division)
    for profile in division.iterdir():
        print(profile.name)
        for content in profile.iterdir():
            if content.is_dir():
                print(f"{profile.name} | {content.name} | Folder")


                #print(f'{content} is a directory.')
            else:
                pass
                #print(f'{content} is a file.')


now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
