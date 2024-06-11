import os

# 用于获取目标目录下的所有的python脚本名称/安装脚本名称


def get_source_list(dir, Filelist):
    if os.path.isfile(dir):
        #print(dir)
        pathlist = dir.split(".")
        if pathlist[-1] == "py":
            Filelist.append(dir)
            # # 若只是要返回文件文，使用这个
            # Filelist.append(os.path.basename(dir))

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue

            newDir = os.path.join(dir, s)
            get_source_list(newDir, Filelist)
    return Filelist


def get_setup_list(dir, Filelist, pkg_name):
    if os.path.isfile(dir):
        pathlist = dir.split("/")
        if pathlist[-1] == "setup.py" and (pathlist[-4] == pkg_name or pathlist[-3] == pkg_name):  # or pathlist[-1] == "__init__.py":
            Filelist.append(dir)
            # # 若只是要返回文件文，使用这个
            # Filelist.append(os.path.basename(dir))

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue

            newDir = os.path.join(dir, s)
            get_setup_list(newDir, Filelist, pkg_name)
    return Filelist


if __name__ == "__main__":
    datashare_path = "/home/banxiangao/Desktop/MPHunter-main/DataShare/Packages"
    pkg_name = "Unpackaged_Packages_0226_0103_corpus_2000"
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