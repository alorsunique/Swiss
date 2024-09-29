import os
from pathlib import Path


def download_sort(download_path,download_sink):
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

    folder_list = ["Documents","Pictures","Music","Videos","Mixed"]

    for folder in folder_list:
        test_dir = download_sink / folder
        if not test_dir.exists():
            os.mkdir(test_dir)


    for files in download_path.iterdir():
        print(files)

        if files.is_file():
            print("File")
        elif files.is_dir():
            print("Dir")




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






    print(download_source_dir)

    download_sort(download_source_dir,download_sink_dir)
    print(download_sink_dir)