import os, subprocess, pickle, sys
import time, gc
from pycg.my_pycg_main import main
from func_timeout import func_set_timeout

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取一个脚本的cg图


@func_set_timeout(20)
def do_func(pyfile, count):
    try:
        print(" ".join([str(count), pyfile.strip()]))
        ret = main(output=PROJECT_DIR + "/DataShare/ApiSeq_and_Result/cg.json", fasten=True,
                   entry_point=[pyfile.strip()])
        # cmd2 = "sed -i '1d' " + data_dir + "/need_analyse_list.txt"
        # os.system(cmd2)
        print("done: " + pyfile)
        return ret[0]
    except Exception as e:
        print(e)
        return ""


def do_process_cg(file_list):
    ret_list = []
    count = 0
    for pyfile in file_list:
        count += 1
        try:
            ret_list.append(do_func(pyfile, count))
        except:
            print("time_out")
    return ret_list


folder = sys.argv[1]
proj_name = sys.argv[2]
id = sys.argv[3]

with open(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/ForMulProcess/" + id + "_target_list.txt", "r") as fp:
    file_list = fp.readlines()

ret_list = do_process_cg(file_list)

with open(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/ForMulProcess/" + id + "_cg_output.txt", "w+") as fp:
    print(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/ForMulProcess/" + id + "_cg_output.txt")
    for i in ret_list:
        fp.write(i)
    fp.write("\n\n")
