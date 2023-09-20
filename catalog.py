# This code should catalog all present accounts in the Otter directory
# It then creates a text file containing every unique user

import os
from datetime import datetime

now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

# Gets the directory of the Python project
project_dir = os.getcwd()

# Change the directory to one level above
split = project_dir.rfind("\\")
new_dir = project_dir[0: split + 1]
os.chdir(new_dir)
working_dir = os.getcwd()

# Takes note of the Otter directory
otter_dir = os.path.join(working_dir, "Otter")

project_folder = []

for division in os.listdir(otter_dir):
    project_folder.append(os.path.join(otter_dir, division))

# Return to the project folder
os.chdir(project_dir)
working_dir = os.getcwd()

directory_count = 0
directory_len = len(project_folder)

valid_account_list = []

for directory in project_folder:
    directory_count += 1

    for entry in os.listdir(directory):
        if entry not in valid_account_list:
            valid_account_list.append(entry)

sorted_list = sorted(valid_account_list)

print(sorted_list)

if os.path.exists(os.path.join(working_dir, "OtterCatalog.txt")):
    os.remove(os.path.join(working_dir, "OtterCatalog.txt"))

catalogObject = open('OtterCatalog.txt', 'w')

for entry in sorted_list:
    catalogObject.write(entry)
    catalogObject.write("\n")

catalogObject.close()

now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
