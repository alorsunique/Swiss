import os
from pathlib import Path

otter_path = Path("D:\Projects\Otter")


account_dict = dict()

for directory in otter_path.iterdir():
    #print(directory)

    for account_dir in directory.iterdir():
        #print(account_dir)
        account = account_dir.name
        account_dict[account] = account_dir

#print(account_dict)