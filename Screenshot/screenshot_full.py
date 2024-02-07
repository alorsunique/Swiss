import os
import time
from datetime import datetime
from pathlib import Path

from PIL import ImageGrab

script_path = Path(__file__).resolve()

print(script_path)

project_dir = script_path.parent.parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

screenshot_dir = resources_dir / "Screenshot"

interval_time = float(input(f"Interval: "))
total_snaps = int(input(f"Amount: "))

len_total_snaps = len(str(total_snaps))

duration = total_snaps * interval_time

current_time = time.time()
sleep_second = 60 - (current_time % 60)

start_time = current_time + sleep_second
end_time = start_time + duration
start_datetime = datetime.fromtimestamp(start_time)
end_datetime = datetime.fromtimestamp(end_time)

print(f"Start: {start_datetime} | End: {end_datetime}")

start_datetime_formatted = start_datetime.strftime("%Y%m%d_%H%M%S")

session_folder = screenshot_dir / f"Session_{start_datetime_formatted}"

if not session_folder.exists():
    os.mkdir(session_folder)

current_time = time.time()
sleep_second = 60 - (current_time % 60)

print(f"Sleeping for {sleep_second}")
time.sleep(sleep_second)

count = 0

while count < total_snaps:
    count += 1

    screenshot_img = ImageGrab.grab()
    current_time = time.strftime("%Y%m%d_%H%M%S")
    screenshot_img.save(session_folder / f"Screenshot_{str(count).zfill(len_total_snaps)}_{current_time}.png")

    time.sleep(interval_time)
