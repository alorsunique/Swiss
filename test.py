import os
from pathlib import Path

otter_path = Path("D:\Projects\Otter")
otter_path = Path("E:\Projects\Otter Archive")

account_dict = dict()

for directory in otter_path.iterdir():
    #print(directory)

    for account_dir in directory.iterdir():
        #print(account_dir)
        account = account_dir.name
        account_dict[account] = account_dir

#print(account_dict)
#print(account_dict.get("yerimiese"))

duplicate_path = Path("E:\Projects\Otter\Le Gras")

for account_dir in duplicate_path.iterdir():
    #print(account_dir)

    potential_duplicate_account_name = account_dir.name
    #print(potential_duplicate_account_name)

    if account_dict.get(potential_duplicate_account_name):


        file_in_otter_list = []

        for file in account_dict.get(potential_duplicate_account_name).iterdir():
            file_in_otter_list.append(file.name)

        file_in_duplicate_list = []

        for file in account_dir.iterdir():
            file_in_duplicate_list.append(file.name)

        print(f"Username: {potential_duplicate_account_name} | Otter Amount: {len(file_in_otter_list)} | Duplicate Amount: {len(file_in_duplicate_list)} | Difference: {len(file_in_otter_list)-len(file_in_duplicate_list)}")

        otter_file_set = set(file_in_otter_list)
        duplicate_file_set = set(file_in_duplicate_list)

        extra_otter_set = otter_file_set.difference(duplicate_file_set)
        extra_duplicate_set = duplicate_file_set.difference(otter_file_set)
        print(f"Extra files in Otter: {len(extra_otter_set)} | Extra files in Duplicate: {len(extra_duplicate_set)}")
        print(extra_duplicate_set)

