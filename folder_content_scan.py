# This should check if folder is empty in Otter directory

import csv
import json
import os
import sys
from datetime import datetime

import numpy as np
from PIL import Image

now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

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

info_dir = os.path.join(working_dir, "Information")

if not os.path.exists(info_dir):
    os.mkdir(info_dir)


directory_count = 0
directory_len = len(project_folder)


for directory in project_folder:
    directory_count += 1
    valid_account_list = []

    for entry in os.listdir(directory):
        valid_account_list.append(entry)

    entry_count = 0
    entry_len = len(valid_account_list)

    for entry in valid_account_list:
        entry_count += 1

        profile_dir = os.path.join(directory, entry)

        if len(os.listdir(profile_dir)) == 0:
            print(entry)
