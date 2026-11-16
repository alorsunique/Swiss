import os
import shutil
import time
from pathlib import Path
import yaml
import sys





def find_project_root(script_path, marker):
    current_path = script_path
    while not (current_path / marker).exists():
        # If block checks for parent of current path
        # If it cannot go up any further, base directory is reached
        if current_path.parent == current_path:
            raise FileNotFoundError(f"Could not find '{marker}' in any parent directories.")

        current_path = current_path.parent

    # If it exits the while loop, marker was found
    return current_path



def storysaver_file_sort(input_to_check_dir, copy_dir):


    for file in input_to_check_dir.rglob('*'):

        if 'storysaver' in str(file.name).lower():
            print(file)

            source_path = file
            copy_storysaver_dir = copy_dir / 'StorySaver'

            copy_path = copy_storysaver_dir / file.name

            similar_count = 0

            if not copy_path.exists():
                shutil.move(source_path, copy_path)

            else:
                while True:
                    print(f'File Name Exists. Adding Number')
                    similar_count += 1
                    new_copy_path = copy_storysaver_dir / f'{file.stem}_{similar_count}{file.suffix}'

                    if not new_copy_path.exists():
                        shutil.move(source_path, new_copy_path)

                        break



def snapinsta_file_sort(input_to_check_dir, copy_dir):


    for file in input_to_check_dir.rglob('*'):

        if 'snapinsta' in str(file.name).lower():
            print(file)

            source_path = file
            copy_snapinsta_dir = copy_dir / 'SnapInsta'

            copy_path = copy_snapinsta_dir / file.name

            similar_count = 0

            if not copy_path.exists():
                shutil.move(source_path, copy_path)

            else:
                while True:
                    print(f'File Name Exists. Adding Number')
                    similar_count += 1
                    new_copy_path = copy_snapinsta_dir / f'{file.stem}_{similar_count}{file.suffix}'

                    if not new_copy_path.exists():
                        shutil.move(source_path, new_copy_path)

                        break




def tiktok_file_sort(input_to_check_dir, copy_dir):

    for file in input_to_check_dir.rglob('*'):

        if 'snaptik' in str(file.name).lower():
            print(file)

            source_path = file
            copy_tiktok_dir = copy_dir / 'Tiktok'

            copy_path = copy_tiktok_dir / file.name

            similar_count = 0

            if not copy_path.exists():
                shutil.move(source_path, copy_path)

            else:
                while True:
                    print(f'File Name Exists. Adding Number')
                    similar_count += 1
                    new_copy_path = copy_tiktok_dir / f'{file.stem}_{similar_count}{file.suffix}'

                    if not new_copy_path.exists():
                        shutil.move(source_path, new_copy_path)

                        break


def RDT_file_sort(input_to_check_dir, copy_dir):

    for file in input_to_check_dir.rglob('*'):

        if 'RDT_' in file.name:

            print(file)

            source_path = file
            copy_reddit_dir = copy_dir / 'Reddit'

            copy_path = copy_reddit_dir / file.name

            similar_count = 0

            if not copy_path.exists():
                shutil.move(source_path, copy_path)

            else:
                while True:
                    print(f'File Name Exists. Adding Number')
                    similar_count += 1
                    new_copy_path = copy_reddit_dir / f'{file.stem}_{similar_count}{file.suffix}'

                    if not new_copy_path.exists():
                        shutil.move(source_path, new_copy_path)

                        break




def screenshot_file_sort(screenshot_in_dir, screenshot_copy_dir):

    for file in screenshot_in_dir.iterdir():

        source_path = file
        copy_path = screenshot_copy_dir / file.name

        if not copy_path.exists():
            shutil.move(source_path, copy_path)



def camera_file_sort(camera_in_dir, camera_raw_dir, camera_vid_dir, lumiere_in_dir):

    for file in camera_in_dir.iterdir():

        source_path = file

        if file.suffix == '.dng':

            copy_path = camera_raw_dir / file.name

        elif file.suffix == '.mp4':

            copy_path = camera_vid_dir / file.name

        else:

            copy_path = lumiere_in_dir / file.name

        if not copy_path.exists():
            shutil.move(source_path, copy_path)



def edited_pic_file_sort(edit_in_dir_list, edit_hold_dir):

    for edit_in_dir in edit_in_dir_list:

        for file in edit_in_dir.iterdir():

            source_path = file
            copy_path = edit_hold_dir / file.name

            similar_count = 0

            if not copy_path.exists():
                shutil.move(source_path, copy_path)

            else:
                while True:
                    print(f'File Name Exists. Adding Number')
                    similar_count += 1
                    new_copy_path = edit_hold_dir / f'{file.stem}_{similar_count}{file.suffix}'

                    if not new_copy_path.exists():
                        shutil.move(source_path, new_copy_path)

                        break




def main():
    config_file_name = 'Inbound_Phone_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)
    sys.path.append(str(project_dir))

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    print(config_content)


    resources_dir = Path( config_content['resources_dir'] )

    inbound_phone_dir = Path( config_content['inbound_phone_dir'] )

    inbound_download_dir = inbound_phone_dir / 'Download'

    copy_dir = resources_dir / 'Inbound_Sort'

    RDT_file_sort(inbound_download_dir, copy_dir)

    inbound_reddit_dir = inbound_phone_dir / 'Reddit'

    RDT_file_sort(inbound_reddit_dir, copy_dir)

    inbound_tiktok_dir = inbound_phone_dir / 'Tiktok'

    tiktok_file_sort(inbound_download_dir, copy_dir)
    tiktok_file_sort(inbound_tiktok_dir, copy_dir)

    snapinsta_file_sort(inbound_download_dir, copy_dir)
    storysaver_file_sort(inbound_download_dir, copy_dir)


    screenshot_in_dir = inbound_phone_dir / 'Screenshots'
    screenshot_copy_dir = Path(config_content['screenshot_copy_dir'])

    screenshot_file_sort(screenshot_in_dir, screenshot_copy_dir)


    camera_in_dir = inbound_phone_dir / 'Camera'
    camera_raw_dir = inbound_phone_dir / 'Camera RAW'
    camera_vid_dir = inbound_phone_dir / 'Camera Video'
    lumiere_in_dir = Path(config_content['lumiere_dir']) / 'Input'

    camera_file_sort(camera_in_dir, camera_raw_dir, camera_vid_dir, lumiere_in_dir)


    edit_in_dir_list = [
        inbound_phone_dir / 'Adobe Express',
        inbound_phone_dir / 'Lightroom',
        inbound_phone_dir / 'Snapseed'
    ]

    lumiere_edit_hold_dir = Path(config_content['lumiere_dir']) / 'Edit Hold'

    edited_pic_file_sort(edit_in_dir_list, lumiere_edit_hold_dir)


if __name__ == "__main__":
    main()