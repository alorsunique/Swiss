import os
import shutil
import time
from pathlib import Path

import pandas as pd


def preliminary_prefix(file_path):
    source_file = file_path

    file_name = source_file.name
    mod_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(os.path.getmtime(source_file)))

    datetime_chunk = mod_time.split(" ")
    date_chunk = datetime_chunk[0].split(":")
    time_chunk = datetime_chunk[1].split(":")
    rename_date = ""
    rename_time = ""
    for chunk in date_chunk:
        rename_date += chunk
    for chunk in time_chunk:
        rename_time += chunk

    modified_name = f"{rename_date}_{rename_time}_{file_name}"
    parent_dir = source_file.parent

    modified_path = parent_dir / modified_name

    os.rename(source_file, modified_path)

    return modified_path


def download_sort(download_source_dir, download_sink_dir, exception_list):
    # Document file extensions
    document_extensions = [
        '.doc', '.docx', '.pdf', '.txt', '.rtf', '.odt', '.xls', '.xlsx',
        '.ppt', '.pptx', '.csv', '.md', '.epub', '.tex'
    ]

    # Image file extensions
    image_extensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg',
        '.webp', '.heic', '.ico', '.psd', '.raw'
    ]

    # Music/Audio file extensions
    music_extensions = [
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma',
        '.aiff', '.alac', '.opus'
    ]

    # Video file extensions
    video_extensions = [
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
        '.m4v', '.mpeg', '.3gp'
    ]

    sink_folder_list = ["Documents", "Pictures", "Music", "Videos", "Everything Else"]

    for folder in sink_folder_list:
        test_dir = download_sink_dir / folder
        if not test_dir.exists():
            os.mkdir(test_dir)

    download_content_list = []

    for entry in download_source_dir.iterdir():
        download_content_list.append(entry)

    content_set = set(download_content_list)
    exception_set = set(exception_list)

    valid_set = content_set - exception_set

    valid_list = sorted(list(valid_set))

    for entry in valid_list:

        modified_path = preliminary_prefix(entry)

        if modified_path.is_file():

            file_extension = modified_path.suffix
            if file_extension in document_extensions:
                move_path = download_sink_dir / "Documents"
            elif file_extension in image_extensions:
                move_path = download_sink_dir / "Pictures"
            elif file_extension in music_extensions:
                move_path = download_sink_dir / "Music"
            elif file_extension in video_extensions:
                move_path = download_sink_dir / "Videos"
            else:
                move_path = download_sink_dir / "Everything Else"


        else:
            move_path = download_sink_dir / "Everything Else"

        shutil.move(modified_path, move_path)


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    download_pointer_path = resources_dir / "Download Pointer.txt"
    with open(download_pointer_path, "r") as download_pointer:
        download_dir_list = download_pointer.read().splitlines()

    download_source_dir = Path(str(download_dir_list[0]).replace('"', ''))
    download_sink_dir = Path(str(download_dir_list[1]).replace('"', ''))

    exception_download_excel_path = resources_dir / "Download Exception.xlsx"

    if not exception_download_excel_path.exists():
        dataframe = pd.DataFrame([], columns=['Exception'])
        dataframe.to_excel(exception_download_excel_path, sheet_name='Exception', index=False)

    dataframe = pd.read_excel(exception_download_excel_path)

    initial_exception_list = dataframe['Exception'].tolist()
    initial_exception_set = set(initial_exception_list)

    sorted_exception_list = sorted(list(initial_exception_set))

    processed_exception_list = []

    for entry in sorted_exception_list:
        processed_exception_list.append(Path(str(entry).replace('"', '')))

    download_sort(download_source_dir, download_sink_dir, processed_exception_list)
