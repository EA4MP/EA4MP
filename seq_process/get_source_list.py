import os

def get_source_list(dir, Filelist):
    if os.path.isfile(dir):
        #print(dir)
        pathlist = dir.split(".")
        if pathlist[-1] == "py":
            Filelist.append(dir)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):

            newDir = os.path.join(dir, s)
            get_source_list(newDir, Filelist)
    return Filelist


def get_setup_list(dir, Filelist, pkg_name):
    if os.path.isfile(dir):
        pathlist = dir.split("/")
        if pathlist[-1] == "setup.py" and (pathlist[-4] == pkg_name or pathlist[-3] == pkg_name):  # or pathlist[-1] == "__init__.py":
            Filelist.append(dir)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_setup_list(newDir, Filelist, pkg_name)
    return Filelist


if __name__ == "__main__":
    datashare_path = ""
    pkg_name = ""
    dir = datashare_path + "/" + pkg_name
    print(dir)
    FileList = get_source_list(dir, [])
    # FileList = get_setup_list(dir, [], pkg_name)
    # with open("../DataShare/Test/cmd.txt", "w+") as file:
    #     for item in FileList:
    #         print(item)
    #         file.write(item + "\n")
    print(len(FileList))
    for item in FileList:
        print(item)
