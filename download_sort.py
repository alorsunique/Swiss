import os
import shutil
from pathlib import Path
import pandas as pd

def download_sort(download_path, download_sink, exception_list):
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

    folder_list = ["Documents", "Pictures", "Music", "Videos", "Mixed"]

    exception_set = set(exception_list)

    print("Exception Set")
    print(exception_set)
    print("----")

    for folder in folder_list:
        test_dir = download_sink / folder
        if not test_dir.exists():
            os.mkdir(test_dir)

    content_list = []

    for content in download_path.iterdir():
        content_list.append(content)

    content_set = set(content_list)

    valid_set = content_set - exception_set
    print(valid_set)

    valid_list = sorted(list(valid_set))

    for entry in valid_list:

        if entry.is_file():
            print(f"File: {entry}")

            relative_path = entry.relative_to(download_path)
            move_path = download_sink / "Documents" / relative_path

            shutil.move(entry, move_path)

        elif entry.is_dir():
            print(f"Dir: {entry}")
        else:
            print("Neither")


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    source_download_pointer_text = resources_dir / "download_pointer_source.txt"
    sink_download_pointer_text = resources_dir / "download_pointer_sink.txt"

    with open(source_download_pointer_text, "r") as download_text:
        download_source_dir = Path(str(download_text.readline()).replace('"', ''))

    with open(sink_download_pointer_text, "r") as download_text:
        download_sink_dir = Path(str(download_text.readline()).replace('"', ''))

    exception_download_excel_path =resources_dir / "Download Exception.xlsx"

    if not exception_download_excel_path.exists():
        dataframe = pd.DataFrame([], columns=['Exception'])
        dataframe.to_excel(exception_download_excel_path, sheet_name='Exception', index=False)

    dataframe = pd.read_excel(exception_download_excel_path)

    initial_exception_list = dataframe['Exception'].tolist()
    initial_exception_set = set(initial_exception_list)

    sorted_exception_list = sorted(list(initial_exception_set))



    #exception_download_text = resources_dir / "exception_list.txt"

    exception_list = sorted_exception_list

    print(exception_list)

    #with open(exception_download_text, "r") as download_text:

        #except_read_list = download_text.readlines()
        #print(except_read_list)
        #print(len(except_read_list))

        #for entry in except_read_list:
            #modified_entry = str(entry).replace('"', '').rstrip('\n')
            #modified_entry = Path(modified_entry)

            #exception_list.append(modified_entry)

    #print(download_source_dir)

    download_sort(download_source_dir, download_sink_dir, exception_list)
    print(download_sink_dir)