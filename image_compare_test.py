import os
from pathlib import Path
import cv2

def feature_matching(image_path_1, image_path_2):
    image_1 = cv2.imread(str(image_path_1, cv2.IMREAD_GRAYSCALE))
    image_2 = cv2.imread(str(image_path_1, cv2.IMREAD_GRAYSCALE))

    sift = cv2.SIFT_create()

    key_points_1, descriptor_1 = sift.detectAndCompute(image_1, None)
    key_points_2, descriptor_2 = sift.detectAndCompute(image_2, None)

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    input_dir = resources_dir / "Input"