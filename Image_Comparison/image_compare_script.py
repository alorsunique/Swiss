import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


import cv2


import itertools
import os
import shutil
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


def streamline_feature_matching(image_path_1, image_path_2):
    image_1 = cv2.imread(str(image_path_1), cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread(str(image_path_2), cv2.IMREAD_GRAYSCALE)

    sift = cv2.SIFT_create()

    key_points_1, descriptor_1 = sift.detectAndCompute(image_1, None)
    key_points_2, descriptor_2 = sift.detectAndCompute(image_2, None)

    FLANN_INDEX_KDTREE = 1
    index_parameters = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_parameters = dict(checks=50)

    FLANN = cv2.FlannBasedMatcher(index_parameters, search_parameters)

    N_neighbors = 2

    matches = FLANN.knnMatch(descriptor_1, descriptor_2, k=N_neighbors)

    match_list = []

    threshold = 0.7

    for a, b in matches:
        if a.distance < threshold * b.distance:
            match_list.append(a)

    minimum_match = 500

    value_list = [len(key_points_1), len(key_points_2), len(match_list)]

    if len(match_list) > minimum_match:
        return True, value_list
    else:
        return False, value_list

    # print(f"Keypoints 1: {len(key_points_1)} | Keypoints 2: {len(key_points_2)} | Matches: {len(match_list)} | {len(match_list)/len(key_points_1)}")




def streamline_feature_matching_flipped(image_path_1, image_path_2):
    image_1 = cv2.imread(str(image_path_1), cv2.IMREAD_GRAYSCALE)
    image_1 = cv2.flip(image_1,1)
    image_2 = cv2.imread(str(image_path_2), cv2.IMREAD_GRAYSCALE)

    sift = cv2.SIFT_create()

    key_points_1, descriptor_1 = sift.detectAndCompute(image_1, None)
    key_points_2, descriptor_2 = sift.detectAndCompute(image_2, None)

    FLANN_INDEX_KDTREE = 1
    index_parameters = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_parameters = dict(checks=50)

    FLANN = cv2.FlannBasedMatcher(index_parameters, search_parameters)

    N_neighbors = 2

    matches = FLANN.knnMatch(descriptor_1, descriptor_2, k=N_neighbors)


    print(type(matches))



    match_list = []

    threshold = 0.7

    for a, b in matches:
        if a.distance < threshold * b.distance:
            match_list.append(a)

    minimum_match = 500

    value_list = [len(key_points_1), len(key_points_2), len(match_list)]

    if len(match_list) > minimum_match:
        return True, value_list
    else:
        return False, value_list











def main():
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent.parent

    # Change working directory to project directory
    os.chdir(project_dir)
    sys.path.append(str(project_dir))


    with open("Resources_Path.txt", "r") as read_text:
        lines = read_text.readlines()

    resources_dir = Path(lines[0].replace('"', ''))

    image_compare_dir = resources_dir / "Image Compare"
    image_posted_dir = image_compare_dir / "Posted"
    image_test_source_dir = image_compare_dir / "Test Source"
    image_probable_source_dir = image_compare_dir / "Probable Source"

    posted_image_list = []

    for entry in image_posted_dir.iterdir():
        posted_image_list.append(entry)

    test_source_list = []

    for entry in image_test_source_dir.iterdir():
        test_source_list.append(entry)

    pair_list = itertools.product(posted_image_list, test_source_list)

    count = 0

    for entry in pair_list:
        count += 1
        print(f"Pair: {count}")
        image_path_1 = entry[0]
        image_path_2 = entry[1]

        copy_condition, value_list = streamline_feature_matching(image_path_1, image_path_2)

        if copy_condition:
            relative_path = image_path_2.relative_to(image_test_source_dir)

            copy_path = image_probable_source_dir / relative_path

            shutil.copy2(image_path_2, copy_path)

        copy_condition, value_list = streamline_feature_matching_flipped(image_path_1, image_path_2)

        if copy_condition:
            relative_path = image_path_2.relative_to(image_test_source_dir)

            copy_path = image_probable_source_dir / relative_path

            shutil.copy2(image_path_2, copy_path)


if __name__ == "__main__":
    main()