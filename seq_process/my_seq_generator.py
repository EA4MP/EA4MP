import pickle
from SourceCode.SequenceGenerator.staticfg.builder import CFGBuilder
from SourceCode.SequenceGenerator.staticfg.staticfg_main import staticfg_main, uncanonical_staticfg_main
from gensim.models import FastText
from gensim.test.utils import datapath
from scipy.spatial.distance import cosine
from SourceCode.SequenceGenerator.pycg.my_pycg_main import main


import os

"""
This file is used to generate the static control flow graph of the python file.
"""

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# /home/banxiangao/Desktop/MPHunter-main
# /media/banxiangao/503A6F9C3A6F7E3A/weekly_update/dcp_24_04_18
# mal_path = "/home/banxiangao/Desktop/MPHunter-main/dataSet/mal"

WE_model_path = datapath("/home/banxiangao/Desktop/MPHunter-main/test/my_model")
print("start to load our model!")
model = FastText.load(WE_model_path)
print("load model successfully")

with open("/home/banxiangao/Desktop/MPHunter-main/test/base_vec.pkl", "rb") as sensitive_func_file:
    base_vec = pickle.load(sensitive_func_file)
    base_vec = [float(x) for x in base_vec]

sensitive_func_file.close()
print(base_vec)


def generate_cg(pyfile, dst_path):
    ret, output_json, filelist, call_list = main(output=dst_path, fasten=True, entry_point=[pyfile])
    return ret, output_json, filelist, call_list


def find_setup_file(folder_path):
    for root, dirs, files in os.walk(folder_path):
        if "setup.py" in files:
            setup_py_path = os.path.join(root, "setup.py")
            return setup_py_path
    return None


def find_largest_file(folder_path, num_files=2):
    py_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                py_files.append((file_path, file_size))

    if not py_files:
        print(f"No py files in {folder_path},please check!")
        return None

    largest_files = sorted(py_files, key=lambda x: x[1], reverse=True)[:num_files]
    return largest_files


def find_top_2_pyfile(folder_path):
    setup_py_path = find_setup_file(folder_path)
    final_path = []
    if setup_py_path:
        print("setup.py file found!")
        final_path.append(setup_py_path)
        largest_files = find_largest_file(folder_path, num_files=2)
        if largest_files and largest_files[0][0] != setup_py_path:
            final_path.append(largest_files[0][0])
        elif largest_files[0][0] != setup_py_path and largest_files[1][0]:
            final_path.append(largest_files[1][0])
    else:
        print(f"did not find setup.py file in {folder_path}")
        largest_files = find_largest_file(folder_path, num_files=2)
        if largest_files:
            final_path.append(largest_files[0][0])
        try:
            if largest_files[1][0]:
                final_path.append(largest_files[1][0])
        except Exception as e:
            print(e)

    return final_path


dfs_diff = 0
bfs_diff = 0
count = 0
folder_path = "/media/banxiangao/503A6F9C3A6F7E3A/weekly_update/dcp_24_04_18"
for file_name in os.listdir(folder_path):
    count += 1
    print(f"start to analysis NO.{count} package!")
    file_path = os.path.join(folder_path, file_name)
    if os.path.isdir(file_path):
        final_files = find_top_2_pyfile(file_path)
        for final_file in final_files:
            path = os.path.basename(final_file)[:-3]
            dst_path = os.path.join(file_path, f"{path}.json")
            print(dst_path)
            try:
                ret, output_json, filelist, call_list = generate_cg(final_file, dst_path)
                dfs_out, bfs_out = staticfg_main([final_file], call_list, model, base_vec)
                # dfs_out_path = os.path.join(folder_path, "dfs_out_con.txt")
                # print(dfs_out_path)
                # bfs_out_path = os.path.join(folder_path, "bfs_out_con.txt")
                e_dfs_out_path = os.path.join(file_path, "dfs_out.txt")
                e_bfs_out_path = os.path.join(file_path, "bfs_out.txt")
                with open(e_dfs_out_path, "a") as e_file_dfs:
                    e_file_dfs.write(dfs_out)
                    e_file_dfs.write("\n")
                e_file_dfs.close()
                with open(e_bfs_out_path, "a") as e_file_bfs:
                    e_file_bfs.write(bfs_out)
                    e_file_bfs.write("\n")
                e_file_bfs.close()
                dfs_out_un, bfs_out_un = uncanonical_staticfg_main([final_file], call_list)
                if dfs_out_un == dfs_out:
                    print("dfs same!")
                else:
                    dfs_diff += 1
                    print("dfs different!")

                if bfs_out_un == bfs_out:
                    print("bfs same!")
                else:
                    bfs_diff += 1
                    print("bfs different!")
            except Exception as e:
                print(e)

print(dfs_diff)
print(bfs_diff)
