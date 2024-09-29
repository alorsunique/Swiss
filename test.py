from pathlib import Path


modified_path = Path("D:\Projects\VS Code\Git Clone Stuff\LibreChat")
unmodified_path = Path("D:\Projects\VS Code\Git Clone Stuff\LibreChat - Copy")


print(modified_path)
print(unmodified_path)


file_in_mod_list = []
dir_in_mod_list = []


for entry in modified_path.rglob('*'):
    if entry.is_file():
        file_in_mod_list.append(entry.relative_to(modified_path))
    elif entry.is_dir():
        dir_in_mod_list.append(entry.relative_to(modified_path))


print(file_in_mod_list)
print(dir_in_mod_list)




file_in_unmod_list = []
dir_in_unmod_list = []


for entry in unmodified_path.rglob('*'):
    if entry.is_file():
        file_in_unmod_list.append(entry.relative_to(unmodified_path))
    elif entry.is_dir():
        dir_in_unmod_list.append(entry.relative_to(unmodified_path))

file_mod_set = set(file_in_mod_list)
file_unmod_set = set(file_in_unmod_list)

dif_set = file_mod_set.intersection(file_unmod_set)
print(dif_set)