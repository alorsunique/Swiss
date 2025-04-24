# This script should find images that are potentially the source of another image

import os
import pickle
import shutil
import sys
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
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

        # print(f"{entry.name} | {(horizontal_size, vertical_size)} | {(new_horizontal, new_vertical)}")

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
def save_sift_data(image_path, sift, mirror_bool):
    loaded_image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

    if mirror_bool:
        loaded_image = cv2.flip(loaded_image, 1)

    key_points, descriptor = sift.detectAndCompute(loaded_image, None)

    return key_points, descriptor


# Feature matching copy paste code.
# Slightly modified
def streamline_feature_matching(key_points_replica, key_points_source, descriptor_replica, descriptor_source):
    FLANN_INDEX_KDTREE = 1
    index_parameters = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_parameters = dict(checks=50)

    FLANN = cv2.FlannBasedMatcher(index_parameters, search_parameters)

    N_neighbors = 2

    if descriptor_replica is None or descriptor_source is None:
        print("One of the descriptor arrays is None.")
        return None, None  # or however you handle a failure case

    if len(descriptor_replica) == 0 or len(descriptor_source) == 0:
        print("One of the descriptor arrays is empty.")
        return None, None  # again, whatever fallback makes sense

    if len(descriptor_source) < N_neighbors:
        print(f"Not enough descriptors in source: {len(descriptor_source)} available, but need {N_neighbors}")
        return None, None

    matches = FLANN.knnMatch(descriptor_replica, descriptor_source, k=N_neighbors)

    match_list = []

    threshold = 0.7

    for a, b in matches:
        if a.distance < threshold * b.distance:
            match_list.append(a)

    minimum_match = 500

    # No clue on what this list does
    value_list = [len(key_points_replica), len(key_points_source), len(match_list)]

    if len(match_list) > minimum_match:
        return True, value_list
    else:
        return False, value_list


# Should check the modification date of the image
def add_replica_mod_time(replica_mod_date_dict, image_file):
    replica_mod_time = os.path.getmtime(image_file)
    replica_mod_date_dict[image_file] = replica_mod_time
    return replica_mod_date_dict


def is_solid_color(image_path):
    test_image = Image.open(image_path).convert('RGB')  # Ensure 3-channel RGB
    image_array = np.array(test_image)

    # Flatten image to 2D array where each row is a pixel (R, G, B)
    pixels = image_array.reshape(-1, image_array.shape[-1])

    # Get first pixel
    first_pixel = pixels[0]

    # Iterate and exit early if a different pixel is found
    for pixel in pixels[1:]:
        if not np.array_equal(pixel, first_pixel):
            return False
    return True


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

    # Removes unnecessary source images

    replica_mod_date_dict = dict()

    for file in replica_dir.iterdir():
        replica_mod_date_dict = add_replica_mod_time(replica_mod_date_dict, file)

    print(max(replica_mod_date_dict, key=replica_mod_date_dict.get))
    print(max(replica_mod_date_dict.values()))
    max_mod_date = max(replica_mod_date_dict.values())

    # Filters through mod time

    for file in source_dir.iterdir():
        source_mod_time = os.path.getmtime(file)
        if source_mod_time > max_mod_date:
            print(f"Later Modification Time | Removing: {file}")
            os.remove(file)


    count = 0

    for file in source_dir.iterdir():
        count += 1
        print(f"Going through source: {count}")
        if is_solid_color(file):
            print(f"Solid Color | Removing: {file}")
            os.remove(file)

    # Rescale the images to not exceed minimum size
    minimum_size = 960

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


    # Pairs up the replica images and source images

    # pair_list = itertools.product(replica_image_list, source_image_list)

    count = 0
    max_count = len(replica_image_list) * len(source_image_list)

    replica_count = 0

    for replica_image_entry in replica_image_list:

        replica_count += 1

        replica_image_path = replica_image_entry

        replica_mod_time = os.path.getmtime(replica_image_path)


        replica_key_points, replica_descriptor = save_sift_data(replica_image_entry, sift, False)
        replica_flip_key_points, replica_flip_descriptor = save_sift_data(replica_image_entry, sift, True)

        source_count = 0

        for source_image_entry in source_image_list:

            source_count += 1

            count += 1
            print(f"Pair: {count} | {max_count} | Replica {replica_count} | Source {source_count}")

            source_image_path = source_image_entry

            source_mod_time = os.path.getmtime(source_image_path)

            if source_mod_time > replica_mod_time:
                print(f"{replica_image_path.name} is older than {source_image_path.name}")

            else:

                source_key_points, source_descriptor = save_sift_data(source_image_entry, sift, False)

                # Compares replica to source

                copy_condition, value_list = streamline_feature_matching(replica_key_points, source_key_points,
                                                                         replica_descriptor, source_descriptor)

                print(copy_condition)

                if copy_condition:
                    probable_source_file_name = source_image_path.name
                    probable_source_path = source_dir / probable_source_file_name

                    replica_folder = probable_dir / replica_image_path.stem

                    if not replica_folder.exists():
                        os.mkdir(replica_folder)

                    copy_path = replica_folder / probable_source_file_name

                    shutil.copy2(probable_source_path, copy_path)

                    replica_copy_file_name = f"Replica_{replica_image_path.name}"
                    replica_copy_path = replica_folder / replica_copy_file_name

                    replica_original_path = replica_dir / replica_image_path.name

                    shutil.copy2(replica_original_path, replica_copy_path)

                # Compares replica flip to source

                copy_condition, value_list = streamline_feature_matching(replica_flip_key_points, source_key_points,
                                                                         replica_flip_descriptor, source_descriptor)

                print(copy_condition)

                if copy_condition:
                    probable_source_file_name = source_image_path.name
                    probable_source_path = source_dir / probable_source_file_name

                    replica_folder = probable_dir / replica_image_path.stem

                    if not replica_folder.exists():
                        os.mkdir(replica_folder)

                    copy_path = replica_folder / probable_source_file_name

                    shutil.copy2(probable_source_path, copy_path)

                    shutil.copy2(probable_source_path, copy_path)

                    replica_copy_file_name = f"Replica_{replica_image_path.name}"
                    replica_copy_path = replica_folder / replica_copy_file_name

                    replica_original_path = replica_dir / replica_image_path.name

                    shutil.copy2(replica_original_path, replica_copy_path)

    # Takes note of ending time
    now = datetime.now()
    finish_time = now
    current_time = now.strftime("%H:%M:%S")
    print(f"Session End Time: {current_time}")
    print(f"Total Session Run Time: {finish_time - start_time}")

    # Removes intermediate folders

    shutil.rmtree(rescaled_replica_dir)
    shutil.rmtree(rescaled_source_dir)
    shutil.rmtree(rescaled_replica_flip_dir)
    shutil.rmtree(data_replica_dir)
    shutil.rmtree(data_source_dir)
    shutil.rmtree(data_replica_flip_dir)


if __name__ == "__main__":
    main()
