# This project will take in images from IG download from selected profiles, rename them accordingly,
# and then move it to another place ready for copying

import os
import shutil

from Modules import mover, modtime

from datetime import datetime

cur_dir = os.getcwd()
environment_dir = os.path.join(cur_dir, "Environment")

#IGDownloadSource_dir = "D:\Projects\PycharmProjects\Capybara"
IGDownloadSource_dir = "D:\Projects\PycharmProjects\DownloadIG"
FromIGSink_dir = "D:\Projects\PycharmProjects\FromIG"

validAccountList = []

now = datetime.now()
startTime = now
current_time = now.strftime("%H:%M:%S")
print("Session Start Time: ", current_time)



for IGProfiles in os.listdir(IGDownloadSource_dir):

    skipCondition = False

    if IGProfiles == ".idea":
        skipCondition = True

    if IGProfiles == "__pycache__":
        skipCondition = True

    if IGProfiles == "Environment":
        skipCondition = True

    if IGProfiles == "venv":
        skipCondition = True

    if not IGProfiles.find(".txt") == -1:
        skipCondition = True

    if not IGProfiles.find(".py") == -1:
        skipCondition = True

    if not IGProfiles.find(".ini") == -1:
        skipCondition = True

    if not skipCondition:
        validAccountList.append(IGProfiles)



if not os.path.exists(FromIGSink_dir):
    os.mkdir(FromIGSink_dir)
else:
    shutil.rmtree(FromIGSink_dir)
    os.mkdir(FromIGSink_dir)


#DownloadIG



catalog_dir = os.path.join(cur_dir, "DownloadIGCatalog.txt")

importFromCatalog = True

if importFromCatalog:
    validAccountList = []

    catalogObject = open(catalog_dir, 'r')
    catalogAccounts = catalogObject.readlines()

    for line in catalogAccounts:
        validAccountList.append(line[:-1])

print(validAccountList)



progressCount = 1
setLength = len(validAccountList)


for validAccount in validAccountList:

    print("Cleaning Environment")

    for toEmpty in os.listdir(environment_dir):
        os.remove(os.path.join(environment_dir, toEmpty))

    # time.sleep(5)

    print("Account: " + validAccount)
    print("Current Progress: " + str(progressCount) + "/" + str(setLength))

    imgsource_dir = os.path.join(IGDownloadSource_dir, validAccount)

    for element in os.listdir(imgsource_dir):
        # print(element)

        if ".jpg" in element:
            imageToTransfer = os.path.join(imgsource_dir, element)

            shutil.copy2(imageToTransfer, environment_dir)

    modtime.prelim_naming(environment_dir)

    indicator = validAccount + "_"

    modtime.mod_renaming(environment_dir, indicator)

    mover.mover(environment_dir, FromIGSink_dir, indicator)

    progressCount += 1



#Capybara



catalog_dir = os.path.join(cur_dir, "CapybaraCatalog.txt")
IGDownloadSource_dir = "D:\Projects\PycharmProjects\Capybara"


importFromCatalog = True

if importFromCatalog:
    validAccountList = []

    catalogObject = open(catalog_dir, 'r')
    catalogAccounts = catalogObject.readlines()

    for line in catalogAccounts:
        validAccountList.append(line[:-1])

print(validAccountList)

progressCount = 1
setLength = len(validAccountList)


for validAccount in validAccountList:

    print("Cleaning Environment")

    for toEmpty in os.listdir(environment_dir):
        os.remove(os.path.join(environment_dir, toEmpty))

    # time.sleep(5)

    print("Account: " + validAccount)
    print("Current Progress: " + str(progressCount) + "/" + str(setLength))

    imgsource_dir = os.path.join(IGDownloadSource_dir, validAccount)

    for element in os.listdir(imgsource_dir):
        # print(element)

        if ".jpg" in element:
            imageToTransfer = os.path.join(imgsource_dir, element)

            shutil.copy2(imageToTransfer, environment_dir)

    modtime.prelim_naming(environment_dir)

    indicator = validAccount + "_"

    modtime.mod_renaming(environment_dir, indicator)

    mover.mover(environment_dir, FromIGSink_dir, indicator)

    progressCount += 1






now = datetime.now()
finishTime = now
current_time = now.strftime("%H:%M:%S")
print("Session End Time: ", current_time)
print("Total Session Run Time: " + str(finishTime - startTime))
