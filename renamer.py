# Renames the file based on an indicator and the time it is modified.

import os

from Modules import mover, modtime

now = modtime.datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

project_dir = os.getcwd()  # Current directory
env_dir = os.path.join(project_dir, "Environment")
move_dir = os.path.join(project_dir, "Move")

# Prepares output folder

if not os.path.exists(env_dir):
    os.mkdir(env_dir)

if not os.path.exists(move_dir):
    os.mkdir(move_dir)

modtime.prelim_naming(env_dir)  # Applies the preliminary rename to content in Environment

indicator = str(input(f"Input your desired indicator: "))
if not indicator == "":
    indicator = f"{indicator}_"

modtime.mod_renaming(env_dir, indicator)  # Performs the final rename to the content in Environment

while True:  # Checks the user if the content should be sorted by file extension
    move_con = str(input(f"Sort the files by extensions? Y/N: "))
    move_con = move_con.upper()
    if move_con == "Y":
        mover.mover(env_dir, move_dir, indicator)
        break
    elif move_con == "N":
        print(f"Files are not moved")
        break
    else:
        print(f"Sorry did not catch that")

now = modtime.datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
