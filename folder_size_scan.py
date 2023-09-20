# This should return the size of the folers in the Otter directory

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


size_csv = os.path.join(info_dir, "Size.csv")

if os.path.exists(size_csv):
    os.remove(size_csv)

creator = open(size_csv, "x")
creator.close()

size_object = open(size_csv, "w", newline='')
size_writer = csv.writer(size_object, delimiter=",")

directory_count = 0
directory_len = len(project_folder)

total_size = 0

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

        size = 0

        for file in os.scandir(profile_dir):
            size += os.path.getsize(file)
            total_size += os.path.getsize(file)


        print_size = float(size)

        partition_count = 0


        while print_size >= 1000:
            print_size /= 1000
            partition_count += 1

        if partition_count == 0:
            partition_text = "B"
        elif partition_count == 1:
            partition_text = "KB"
        elif partition_count == 2:
            partition_text = "MB"
        elif partition_count == 3:
            partition_text = "GB"

        print_size_string = str(round(print_size, 2))

        print(f"{entry} | {print_size_string} {partition_text}")


partition_count = 0
print_size = total_size

while print_size >= 1000:
    print_size /= 1000
    partition_count += 1

if partition_count == 0:
    partition_text = "B"
elif partition_count == 1:
    partition_text = "KB"
elif partition_count == 2:
    partition_text = "MB"
elif partition_count == 3:
    partition_text = "GB"

print_size_string = str(round(print_size, 2))

print(f"Total | {print_size_string} {partition_text}")