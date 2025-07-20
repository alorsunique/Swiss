# This script is for taking the source image in move set and create a copy of it in the Swiss directory
# Purpose is to just take note where the image came from
# The image is stored but this is for credit purposes

import os
from pathlib import Path
import sys
import shutil






def get_account_id_json(move_set_reference_dir, otter_dir):

    account_list = []

    for content in move_set_reference_dir.iterdir():

        if content.is_dir():
            account_list.append(content.name)

    print(account_list)

    for working_account in account_list:

        for category in otter_dir.iterdir():

            # print(category)
            check_account_dir = category / working_account
            # print(check_account_dir)

            if check_account_dir.exists():

                account_number_id = ''

                for entry in check_account_dir.rglob('*.xz'):
                    if str(working_account) in str(entry.name):
                        print(entry)
                        account_number_id = str(entry.name).replace(f'{working_account}_','')
                        print(account_number_id)

                json_list = []

                for entry in check_account_dir.rglob('*.xz'):
                    if account_number_id in str(entry.name):
                        json_list.append(entry)

                print(json_list)


                for entry in json_list:
                    print(entry)
                    copy_folder = move_set_reference_dir / working_account

                    print(copy_folder)

                    copy_path = copy_folder / entry.name
                    print(f'COPY PATH {copy_path}')

                    shutil.copy2(entry, copy_path)








def otter_sourcing(source_list, move_set_reference_dir, otter_dir):


    for category in otter_dir.iterdir():

        for account in category.iterdir():


            for entry in source_list:



                check_path = account / entry

                if check_path.exists():
                    print(f"{check_path} | Image found")


                    copy_folder = move_set_reference_dir / account.name

                    if not copy_folder.exists():
                        os.mkdir(copy_folder)

                    copy_path = copy_folder / entry
                    shutil.copy2(check_path, copy_path)
                else:
                    print(f"{check_path} | Image not found")



def main():
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent

    # Change working directory to project directory
    os.chdir(project_dir)
    sys.path.append(str(project_dir))


    with open("Resources_Path.txt", "r") as read_text:
        lines = read_text.readlines()

    resources_dir = Path(lines[0].replace('"', ''))

    move_set_reference_dir =  resources_dir / "Move Set Reference"

    if not move_set_reference_dir.exists():
        os.mkdir(move_set_reference_dir)

    move_set_pointer_text = resources_dir / "Move_Set_Pointer.txt"

    with open(move_set_pointer_text, "r") as read_text:
        lines = read_text.readlines()

    move_set_dir = Path(str(lines[0]).replace('"', ''))

    print(move_set_dir)

    otter_dir = Path("F:\Projects\Otter")

    post_list = []

    source_list = []

    for content in move_set_dir.iterdir():

        if content.is_dir():

            post_name = content.name




            for subcontent in content.iterdir():
                if post_name in str(subcontent.name):
                    post_list.append(subcontent.name)
                else:
                    source_list.append(subcontent.name)

                print(subcontent)

    otter_sourcing(source_list, move_set_reference_dir, otter_dir)

    get_account_id_json(move_set_reference_dir, otter_dir)

if __name__ == "__main__":
    main()

