# This script should find images that are potentially the source of another image

import itertools
import os
import pickle
import shutil
import sys
from datetime import datetime
from pathlib import Path

import cv2
from PIL import Image, ImageOps


# Resizes function
def tree_resize_image(input_dir, rescale_dir, minimum_size, mirror_bool):
    min_size = minimum_size
    image_list = []
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    for entry in input_dir.rglob('*'):
        if entry.is_file and str(entry).endswith(image_extensions):
            image_list.append(entry)

    for entry in image_list:
        working_image = Image.open(entry)

        horizontal_size = working_image.size[0]
        vertical_size = working_image.size[1]

        min_pixel_size = min(working_image.size)

        if min_pixel_size > min_size:
            rescale_factor = min_pixel_size / min_size
            new_horizontal = int(horizontal_size / rescale_factor)
            new_vertical = int(vertical_size / rescale_factor)
        else:
            new_horizontal = horizontal_size
            new_vertical = vertical_size

        print(f"{entry.name} | {(horizontal_size, vertical_size)} | {(new_horizontal, new_vertical)}")

        relative_dir = entry.relative_to(input_dir).parent
        output_dir = rescale_dir / relative_dir

        if not output_dir.exists():
            os.makedirs(output_dir)

        output_path = output_dir / entry.name
        rescaled_image = working_image.resize((new_horizontal, new_vertical), Image.LANCZOS)

        if mirror_bool:
            rescaled_image = ImageOps.mirror(rescaled_image)

        rescaled_image.save(str(output_path))

        rescaled_image.close()
        working_image.close()

        mod_time = os.path.getmtime(entry)
        os.utime(output_path, (mod_time, mod_time))


# Function to save key points and descriptor
def save_sift_data(image_path, key_point_path, descriptor_path, sift, mirror_bool):
    loaded_image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

    if mirror_bool:
        loaded_image = cv2.flip(loaded_image, 1)

    key_points, descriptor = sift.detectAndCompute(loaded_image, None)

    # Serializes the key points so that it can be saved to a file
    key_points_serialized = [
        (kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in key_points
    ]

    with open(key_point_path, 'wb') as data_dump:
        pickle.dump(key_points_serialized, data_dump)

    with open(descriptor_path, 'wb') as data_dump:
        pickle.dump(descriptor, data_dump)


def load_sift_data(key_point_path, descriptor_path):
    # Loads the serialized key points
    with open(key_point_path, 'rb') as data_dump:
        key_points_serialized = pickle.load(data_dump)

    # Reconstruct the cv2.KeyPoint objects
    loaded_key_points = [
        cv2.KeyPoint(x=pt[0], y=pt[1], size=size, angle=angle, response=response, octave=octave, class_id=class_id)
        for (pt, size, angle, response, octave, class_id) in key_points_serialized
    ]

    # Converts the key point list to tuple
    key_points = tuple(loaded_key_points)

    # Load the descriptors
    with open(descriptor_path, 'rb') as data_dump:
        descriptor = pickle.load(data_dump)

    return key_points, descriptor


# Feature matching copy pasted code.
# Slightly modified
def streamline_feature_matching(key_points_1, key_points_2, descriptor_1, descriptor_2):
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

    # No clue on what this list does
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

    # Takes note of starting time
    now = datetime.now()
    start_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Session Start Time: {current_time}")

    with open("Resources_Path.txt", "r") as read_text:
        lines = read_text.readlines()

    resources_dir = Path(lines[0].replace('"', ''))

    # Important directories
    image_compare_dir = resources_dir / "Image Compare"
    replica_dir = image_compare_dir / "Replica"
    source_dir = image_compare_dir / "Source"
    probable_dir = image_compare_dir / "Probable"

    if not replica_dir.exists():
        os.makedirs(replica_dir)

    if not source_dir.exists():
        os.makedirs(source_dir)

    if not probable_dir.exists():
        os.makedirs(probable_dir)

    # Creates the rescale directories
    rescaled_replica_dir = image_compare_dir / "Rescaled Replica"
    rescaled_source_dir = image_compare_dir / "Rescaled Source"
    rescaled_replica_flip_dir = image_compare_dir / "Rescaled Replica Flip"

    if rescaled_replica_dir.exists():
        shutil.rmtree(rescaled_replica_dir)
    os.mkdir(rescaled_replica_dir)

    if rescaled_source_dir.exists():
        shutil.rmtree(rescaled_source_dir)
    os.mkdir(rescaled_source_dir)

    if rescaled_replica_flip_dir.exists():
        shutil.rmtree(rescaled_replica_flip_dir)
    os.mkdir(rescaled_replica_flip_dir)

    # Rescale the images to not exceed minimum size
    minimum_size = 1080

    tree_resize_image(replica_dir, rescaled_replica_dir, minimum_size, False)
    tree_resize_image(source_dir, rescaled_source_dir, minimum_size, False)
    tree_resize_image(replica_dir, rescaled_replica_flip_dir, minimum_size, True)

    # Takes note of rescaled replica images
    replica_image_list = []

    for entry in rescaled_replica_dir.iterdir():
        replica_image_list.append(entry)

    # Takes note of rescaled source images
    source_image_list = []

    for entry in rescaled_source_dir.iterdir():
        source_image_list.append(entry)

    # Takes note of rescaled flip replica images
    replica_flip_image_list = []

    for entry in rescaled_replica_flip_dir.iterdir():
        replica_flip_image_list.append(entry)

    # Creates the directory for the sift data
    data_replica_dir = image_compare_dir / "Data Replica"
    data_source_dir = image_compare_dir / "Data Source"
    data_replica_flip_dir = image_compare_dir / "Data Replica Flip"

    if data_replica_dir.exists():
        shutil.rmtree(data_replica_dir)
    os.mkdir(data_replica_dir)

    if data_source_dir.exists():
        shutil.rmtree(data_source_dir)
    os.mkdir(data_source_dir)

    if data_replica_flip_dir.exists():
        shutil.rmtree(data_replica_flip_dir)
    os.mkdir(data_replica_flip_dir)

    # Determines the key points and descriptor

    sift = cv2.SIFT_create()

    for image in replica_image_list:
        key_path = data_replica_dir / f"Key_{image.stem}.pkl"
        data_path = data_replica_dir / f"Descriptor_{image.stem}.pkl"

        save_sift_data(image, key_path, data_path, sift, False)

    for image in source_image_list:
        key_path = data_source_dir / f"Key_{image.stem}.pkl"
        data_path = data_source_dir / f"Descriptor_{image.stem}.pkl"

        save_sift_data(image, key_path, data_path, sift, False)

    for image in replica_image_list:
        key_path = data_replica_flip_dir / f"Key_{image.stem}.pkl"
        data_path = data_replica_flip_dir / f"Descriptor_{image.stem}.pkl"

        save_sift_data(image, key_path, data_path, sift, True)

    # Pairs up the replica images and source images

    pair_list = itertools.product(replica_image_list, source_image_list)

    count = 0

    for entry in pair_list:
        count += 1
        print(f"Pair: {count}")
        replica_image_path = entry[0]
        source_image_path = entry[1]

        replica_key_path = data_replica_dir / f"Key_{replica_image_path.stem}.pkl"
        replica_descriptor_path = data_replica_dir / f"Descriptor_{replica_image_path.stem}.pkl"

        source_key_path = data_source_dir / f"Key_{source_image_path.stem}.pkl"
        source_descriptor_path = data_source_dir / f"Descriptor_{source_image_path.stem}.pkl"

        replica_flip_key_path = data_replica_flip_dir / f"Key_{replica_image_path.stem}.pkl"
        replica_flip_descriptor_path = data_replica_flip_dir / f"Descriptor_{replica_image_path.stem}.pkl"

        key_points_1, descriptor_1 = load_sift_data(replica_key_path, replica_descriptor_path)
        key_points_2, descriptor_2 = load_sift_data(source_key_path, source_descriptor_path)
        key_points_3, descriptor_3 = load_sift_data(replica_flip_key_path, replica_flip_descriptor_path)

        # Compares replica to source

        copy_condition, value_list = streamline_feature_matching(key_points_1, key_points_2, descriptor_1, descriptor_2)

        print(copy_condition)

        if copy_condition:
            probable_source_file_name = source_image_path.name
            probable_source_path = source_dir / probable_source_file_name
            copy_path = probable_dir / probable_source_file_name

            shutil.copy2(probable_source_path, copy_path)

        # Compares replica flip to source

        copy_condition, value_list = streamline_feature_matching(key_points_1=key_points_3, key_points_2=key_points_2, descriptor_1=descriptor_3, descriptor_2=descriptor_2)

        #print(copy_condition)

        #if copy_condition:
            #probable_source_file_name = source_image_path.name
            #probable_source_path = source_dir / probable_source_file_name
            #copy_path = probable_dir / probable_source_file_name

            #shutil.copy2(probable_source_path, copy_path)

    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Session End Time: {current_time}")
    print(f"Total Session Run Time: {finish_time - start_time}")

    # Removes intermediate folders

    # shutil.rmtree(rescaled_replica_dir)
    # shutil.rmtree(rescaled_source_dir)
    # shutil.rmtree(data_replica_dir)
    # shutil.rmtree(data_source_dir)


if __name__ == "__main__":
    main()
