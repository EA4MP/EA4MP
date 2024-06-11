from SourceCode.SequenceGenerator import get_source_list
import os, subprocess, pickle
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED, as_completed
import time, gc
from SourceCode.SequenceGenerator.pycg.my_pycg_main import main
from SourceCode.SequenceGenerator.staticfg.staticfg_main import staticfg_main
from gensim.models import FastText
from gensim.test.utils import datapath
from func_timeout import func_set_timeout
from multiprocessing import Pool

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(PROJECT_DIR)
OUTPUT_LINE = []
OUTPUT_LINE_CFG_DFS = []
OUTPUT_LINE_CFG_BFS = []
COUNT = 0
# ################# for threadpool #########################################
import queue

class BoundThreadPoolExecutor(ThreadPoolExecutor):

    def __init__(self, *args, **kwargs):
        super(BoundThreadPoolExecutor, self).__init__(*args, **kwargs)
        self._work_queue = queue.Queue(400)
#############################################################################


#####################################################################################################################
# main functions: 获得一个脚本的API调用序列
#####################################################################################################################

def do_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True)
    print("wait")
    p.wait()
    p.kill()


def get_seq_main(datashare_path, package_name, folder, proj_name, model_dir,
                 WE_model_name, WE_proj_name, mode, file_search_mode,
                 graph_mode, task_num):
    if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/"):
        os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/")
    if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess"):
        os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess")
    if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result"):
        os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result")
    if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + ""):
        os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "")
    if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name):
        os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name)
    if graph_mode == "cfg+cg" or graph_mode == "dfs":
        for_mul_process_folder_path = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + \
                                      folder + "/" + proj_name + "/ForMulProcess_cfg"
    elif graph_mode == "cg":
        for_mul_process_folder_path = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + \
                                      folder + "/" + proj_name + "/ForMulProcess"
    if not os.path.exists(for_mul_process_folder_path):
        os.mkdir(for_mul_process_folder_path)
    data_dir = datashare_path + "/" + package_name
    print(data_dir)
    if file_search_mode == "setup_only":
        FileList = get_source_list.get_setup_list(data_dir, [], package_name)
    elif file_search_mode == "all_files":
        FileList = get_source_list.get_source_list(data_dir, [])
    # print(FileList)
    print(len(FileList))
    divided_file_lists = []
    temp = []
    i = 0
    id = 0
    with open(data_dir + "/need_analyse_list.txt", "w+") as file:
        for pyfile in FileList:
            file.write(pyfile + "\n")
    for pyfile in FileList:
        temp.append(pyfile)
        i += 1
        if len(temp) >= 10000 or i == len(FileList):
            id += 1
            divided_file_lists.append(temp)
            with open(for_mul_process_folder_path + "/" + str(id) + "_target_list.txt", "w+") as fp:
                for line in temp:
                    fp.write(line.strip() + "\n")
            temp = []
            # break  # needs to be removed

    if graph_mode == "cfg+cg":
        traverse_graph(len(divided_file_lists), task_num, [datashare_path, package_name, folder, proj_name, model_dir,
                       WE_model_name, WE_proj_name, mode], ["cg_", "dfs_", "bfs_"], folder,
                       proj_name, "do_single_process_cfg.py", for_mul_process_folder_path)
    elif graph_mode == "cg":
        traverse_graph(len(divided_file_lists), task_num, [folder, proj_name], ["cg_"], folder,
                       proj_name, "do_single_process_cg.py", for_mul_process_folder_path)
        output_path = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/"
        os.rename(output_path + "cg_output.txt", output_path + "output.txt")


def traverse_graph(batch_num, task_num, arg_list, prefix_list, folder, proj_name,
                   processor_name, for_mul_process_folder_path):
    count = 0
    cmd_list = []
    for i in range(batch_num):
        count += 1
        long_para = " ".join(arg_list) + " " + str(i + 1)
        cmd_list.append("python3 " + PROJECT_DIR + "/SequenceGenerator/" + processor_name + " " + long_para)

    with Pool(task_num) as pool:
        pool.map(do_cmd, cmd_list)
    print("get graph : done")

    for prefix in prefix_list:

        if prefix == "dfs_":
            output_prefix = ""
        else:
            output_prefix = prefix
        output_file = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + \
                      "/" + output_prefix + "output.txt"
        cmd = "cd " + for_mul_process_folder_path + "; cat *_" + prefix + "output.txt > " + output_file
        os.system(cmd)
