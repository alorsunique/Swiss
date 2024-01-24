import os
import time
from pathlib import Path

from PIL import ImageGrab

project_dir = Path.cwd().parent
os.chdir(project_dir)

with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(resources_text.readline())

screenshot_dir = resources_dir / "Screenshot"


def next_min_sleep():
    current_time = time.time()
    sleep_second = 60 - (current_time % 60)

    print(f"Sleeping for {sleep_second}")
    time.sleep(sleep_second)


next_min_sleep()

while True:
    screenshot_img = ImageGrab.grab()
    current_time = time.strftime("%Y%m%d_%H%M%S")
    screenshot_img.save(screenshot_dir / f"Screenshot_{current_time}.png")
    time.sleep(2)
