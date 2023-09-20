# This should check for corrupted images in the Capybara and DownloadIG folders

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
current_dir = project_dir


# Change the directory to one level above
split = current_dir.rfind("\\")
new_dir = current_dir[0: split + 1]
os.chdir(new_dir)
working_dir = os.getcwd()

current_dir = working_dir

# Change the directory to one level above
split = current_dir.rfind("\\")
new_dir = current_dir[0: split + 1]
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

pass_through_dir = os.path.join(info_dir, "Pass Through")

if not os.path.exists(pass_through_dir):
    os.mkdir(pass_through_dir)

corrupted_csv = os.path.join(info_dir, "Corrupted.csv")

if os.path.exists(corrupted_csv):
    os.remove(corrupted_csv)

creator = open(corrupted_csv, "x")
creator.close()

corrupted_object = open(corrupted_csv, "w", newline='')
corrupted_writer = csv.writer(corrupted_object, delimiter=",")

directory_count = 0
directory_len = len(project_folder)

error_count = 0

for directory in project_folder:
    directory_count += 1
    valid_account_list = []

    for entry in os.listdir(directory):
        valid_account_list.append(entry)

    # new_valid_account_list = [valid_account_list[0]]

    entry_count = 0
    entry_len = len(valid_account_list)
    # entry_len = len(new_valid_account_list)

    # for entry in new_valid_account_list:
    for entry in valid_account_list:
        print(entry)
        entry_count += 1
        profile_dir = os.path.join(directory, entry)

        clean_pack = []

        profile_JSON_dir = os.path.join(pass_through_dir, f"{entry}.json")
        if os.path.exists(profile_JSON_dir):
            json_file = open(profile_JSON_dir, "r")
            data = json.load(json_file)
            clean_pack = data
            json_file.close()

        # print(f"Pass Through Size: {clean_pack}")

        json_file = open(profile_JSON_dir, "w")

        image_pack = []

        file_count = 0
        file_len = len(os.listdir(profile_dir))
        for file in os.listdir(profile_dir):
            file_count += 1
            if ".jpg" in file and file not in clean_pack:
                directory_frac = f"{directory_count}/{directory_len}"
                entry_frac = f"{entry_count}/{entry_len}"
                file_frac = f"{file_count}/{file_len}"
                sys.stdout.write(f"\rDirectory: {directory_frac} | Account: {entry_frac} | File: {file_frac}")

                img_dir = os.path.join(profile_dir, file)
                try:
                    img = Image.open(img_dir)  # Open the image file

                    # Performs the check here. If no error happens, the image is good.
                    img_arr = np.array(img)
                    img.close()

                    clean_pack.append(file)

                except (IOError, SyntaxError) as e:
                    error_count += 1
                    image_pack.append(file)
        if len(image_pack) > 0:
            write_pack = [directory, entry, image_pack]
            corrupted_writer.writerow(write_pack)

        clean_copy_pack = clean_pack.copy()

        for corrupted in image_pack:
            corrupted_split = corrupted.split("_")
            corrupted_string = f"{corrupted_split[0]}_{corrupted_split[1]}"
            print(f"Corrupted String: {corrupted_string}")

            for clean in clean_copy_pack:
                if corrupted_string in clean:
                    print(f"Removing Clean: {clean} | Corresponding Corrupt: {corrupted} | String: {corrupted_string}")
                    clean_pack.remove(clean)

        json.dump(clean_pack, json_file)
        json_file.close()

sys.stdout.write(f"\rComplete. Corrupted Images Found: {error_count}\n")

now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
