# Renames video

import os

project_dir = os.getcwd()
environment_dir = os.path.join(project_dir, "Environment")

if not os.path.exists(environment_dir):
    os.mkdir(environment_dir)

run_condition = input(f"Select Y to perform a run through: ").upper()

if run_condition == "Y":

    for runThrough in os.listdir(environment_dir):
        src_file = os.path.join(environment_dir, runThrough)

        split_tup = os.path.splitext(runThrough)

        title_string = split_tup[0]

        if title_string[-1] != ")":
            break

        countdown = len(title_string)

        while True:
            countdown -= 1
            if title_string[countdown] == "(":
                break

        title_string = title_string[:countdown - 1]

        new_filename_string = title_string + split_tup[1]
        new_filename = os.path.join(environment_dir, new_filename_string)
        os.rename(src_file, new_filename)

for show_new in os.listdir(environment_dir):
    print(f"Run Through Results: {show_new}")

front_string_remove = input(f'Front String: ')
back_string_remove = input(f'Back String: ')

for videos in os.listdir(environment_dir):
    print(f"Initial: {videos}")

    src_file = os.path.join(environment_dir, videos)

    split_tup = os.path.splitext(videos)

    title_hold1 = split_tup[0]

    title_hold2 = title_hold1.replace(front_string_remove, '')
    title_string = title_hold2.replace(back_string_remove, '')

    new_filename_string = title_string + split_tup[1]
    print(f"Final: {new_filename_string}")

    new_filename = os.path.join(environment_dir, new_filename_string)

    # print(newFileName)

    os.rename(src_file, new_filename)
