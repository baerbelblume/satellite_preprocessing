## A. Barbara Metzler
## 13. November 2019
## script to get the names of the tif images in a list

import os

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def main():
    file_list = []
    # name of folder with imagery data
    dirName = '../Accra/all_tif_files/';

    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)

    # Print the files
    #for elem in listOfFiles:
    #    print(elem)

    #print ("****************")

    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    # Print the files
    for elem in listOfFiles:
        if elem.endswith(".tif"):
            file_list.append(elem)
    return(file_list)


if __name__ == '__main__':
    main()
