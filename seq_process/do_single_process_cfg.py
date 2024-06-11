from pycg.my_pycg_main import main
from staticfg.staticfg_main import staticfg_main
from gensim.models import FastText
from gensim.test.utils import datapath
from func_timeout import func_set_timeout
import os, pickle, sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PROJECT_DIR)


@func_set_timeout(30)
def uncanonical_do_func(pyfile):
    try:
        cg_ret = main(output=PROJECT_DIR + "/DataShare/ApiSeq_and_Result/cg.json", fasten=True,
                  entry_point=[pyfile])
        # print(ret_list)
        # cmd2 = "sed -i '1d' " + data_dir + "/need_analyse_list.txt"
        # os.system(cmd2)
        file_list = cg_ret[2]
        call_dict = cg_ret[3]
        print(pyfile + " cgfile_list_len:" + str(len(file_list)))
        cfg_dfs_ret, cfg_bfs_ret = staticfg_main(file_list, call_dict)
        return cg_ret, cfg_dfs_ret, cfg_bfs_ret
    except Exception as e:
        print("Exception!")
        print(e)
        return [""], "", ""


@func_set_timeout(30)
def do_func(pyfile, model, sensitive_func_v_list):
    try:
        cg_ret = main(output=PROJECT_DIR + "/DataShare/ApiSeq_and_Result/cg.json", fasten=True,
                  entry_point=[pyfile])
        # print(ret_list)
        # cmd2 = "sed -i '1d' " + data_dir + "/need_analyse_list.txt"
        # os.system(cmd2)
        file_list = cg_ret[2]
        call_dict = cg_ret[3]
        print(pyfile + " cgfile_list_len:" + str(len(file_list)))
        cfg_dfs_ret, cfg_bfs_ret = staticfg_main(file_list, call_dict, model, sensitive_func_v_list)
        return cg_ret, cfg_dfs_ret, cfg_bfs_ret
    except Exception as e:
        print("Exception!")
        print(e)
        return [""], "", ""


def do_process_cg_cfg(file_list, data_dir, model=None, sensitive_func_v_list=None):
    ret_list = []
    print(len(file_list))
    COUNT = 0
    for pyfile in file_list:
        COUNT += 1
        print(str(COUNT))
        pyfile = pyfile.strip()
        print(pyfile)
        try:
            cg_ret, cfg_dfs_ret, cfg_bfs_ret = do_func(pyfile, model, sensitive_func_v_list)
            ret_list.append([cg_ret[0], cfg_dfs_ret, cfg_bfs_ret])
            print("done:" + pyfile)
        except Exception as e:
            print(e)

    return ret_list


def load_WE_model(model_dir, WE_model_name, WE_proj_name, mode):

    WE_model_file_dir = datapath("/home/banxiangao/Desktop/MPHunter-main/test/my_model")
    print("model loading: start\n\nPlease wait patiently\n")
    model = FastText.load(WE_model_file_dir)
    print("model loading: complete")

    with open("/home/banxiangao/Desktop/MPHunter-main/test/base_vec.pkl", "rb") as sensitive_func_file:
        base_vec = pickle.load(sensitive_func_file)
        base_vec = [float(x) for x in base_vec]

    return model, [base_vec]


def do_cmd_process_main(datashare_path, package_name, folder, proj_name, model_dir, WE_model_name,
                        WE_proj_name, mode, file_list, id):

    model, sensitive_func_v_list = load_WE_model(model_dir, WE_model_name, WE_proj_name, mode)

    data_dir = datashare_path + "/" + package_name
    ret_list = do_process_cg_cfg(file_list, data_dir, model, sensitive_func_v_list)

    ################
    fp_cg = open("/home/banxiangao/Desktop/MPHunter-main/test" + id + "_cg_output.txt", "w+")
    fp_dfs = open("/home/banxiangao/Desktop/MPHunter-main/test" + id + "_dfs_output.txt", "w+")
    fp_bfs = open("/home/banxiangao/Desktop/MPHunter-main/test" + id + "_bfs_output.txt", "w+")
    print("/home/banxiangao/Desktop/MPHunter-main/test" + id + "_output.txt")
    for i in ret_list:
        fp_cg.write(i[0])
        fp_dfs.write(i[1])
        fp_bfs.write(i[2])
    fp_cg.write("\n\n")
    fp_dfs.write("\n\n")
    fp_bfs.write("\n\n")

    fp_bfs.close()
    fp_dfs.close()
    fp_cg.close()

def uncanonical_do_cmd_process_main(datashare_path, package_name, folder, proj_name, model_dir, WE_model_name,
                        WE_proj_name, mode, file_list, id):

    data_dir = datashare_path + "/" + package_name
    ret_list = do_process_cg_cfg(file_list, data_dir)

    ################
    fp_cg = open(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name +
                 "/ForMulProcess_cfg/" + id + "_cg_output.txt", "w+")
    fp_dfs = open(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name +
                  "/ForMulProcess_cfg/" + id + "_dfs_output.txt", "w+")
    fp_bfs = open(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name +
                  "/ForMulProcess_cfg/" + id + "_bfs_output.txt", "w+")
    print(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/ForMulProcess_cfg/" +
          id + "_output.txt")
    for i in ret_list:
        fp_cg.write(i[0])
        fp_dfs.write(i[1])
        fp_bfs.write(i[2])
    fp_cg.write("\n\n")
    fp_dfs.write("\n\n")
    fp_bfs.write("\n\n")

    fp_bfs.close()
    fp_dfs.close()
    fp_cg.close()

print("do single process cfg")
datashare_path = sys.argv[1]
pkg_name = sys.argv[2]
folder = sys.argv[3]
proj_name = sys.argv[4]
model_dir = sys.argv[5]
WE_model_name = sys.argv[6]
WE_proj_name = sys.argv[7]
method = sys.argv[8]
id = 1

data_dir = datashare_path + "/" + pkg_name
# print(data_dir)
file_list = []


with open(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name +
          "/ForMulProcess_cfg/" + id + "_target_list.txt", "r") as fp:
    file_list = fp.readlines()
    # print(file_list)
do_cmd_process_main(datashare_path, pkg_name, folder, proj_name, model_dir, WE_model_name, WE_proj_name, method, file_list, id)
