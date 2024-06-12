
from SourceCode.SequenceGenerator.pycg.my_pycg_main import main

import os
import tarfile
import shutil


dst_dir = ""
def scan_file(path_dir):
    filenames = tuple([os.path.join(path_dir, f) for f in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))])
    # for filename in filenames:
    #     print(filename)
    return filenames

def decompression(file_path):
    if file_path.endswith(".tar.gz"):
        try:
            with tarfile.open(file_path,'r:gz') as tar:
                tar.extractall(path=os.path.dirname(file_path))
                print(f"successfully decompression {file_path}")
        except Exception as e:
            print(f"unsuccessfully decompression {file_path} since : {e}")

    else:
        print(f"{file_path} is not a targz file,skipping!")

def move_py_file(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_dir, file)
                shutil.move(src_file, dst_file)
                print(f"move {src_file} to {dst_file} successfully!")

# filenames = scan_file(PATH)
# for filename in filenames:
#     file_path = os.path.join(PATH, filename)
#     if os.path.isfile(file_path):
#         decompression(file_path)
#
#
# move_py_file(PATH, dst_dir)

final_dir = ""
pyfile_dir = ""
pyfile_names = scan_file(pyfile_dir)
ret_list = []
sum = 1
sum_success = 0
sum_default = 0
# length of pyfile_names is 57369
for pyfile_name in pyfile_names:
    print(f"start to analysis no.{sum} pyfile {os.path.basename(pyfile_name)}")
    try:
        # print(os.path.basename(pyfile_name))
        pyfile_path = os.path.join(pyfile_dir, pyfile_name)
        # print(pyfile_path)
        final_path = os.path.join(final_dir, os.path.basename(pyfile_name)[:-3]+"_cg.json")
        # print(final_path)
        ret, output_json, filelist, call_list = main(output=final_path, fasten=True, entry_point=[pyfile_path])
        ret_list.append(ret)
        sum_success += 1
        print(f"sunccess to analysis no.{sum} pyfile,total success {sum_success}")
        sum += 1
        # print(ret)
    except Exception as e:
        print("error!", e)
        sum_default += 1
        print(f"default to analysis no.{sum} pyfile, total default {sum_default}")
        sum += 1
    # print(filelist)

count = 0
print(sum_default)
print(sum_success)
with open("", "a") as fp:
    for i in ret_list:
        fp.write(i)
        count += 1
        if count % 100 == 0:
            print(f"have already finish write {count} cg information")
    fp.write("\n\n")

fp.close()


# scan_file(PATH)
