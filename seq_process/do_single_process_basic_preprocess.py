import os
import os, pickle, gc, shutil
import sys
from basic_preprocess_main import Preprocessor

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class cmd_preprocessor(Preprocessor):
    def seq_preprocess_mul_process_main(self, min_len=0, output_file_name="output_connected.txt", proj_name="test",
                                        folder="WordEmbedding", method="ft", target_file_list=["setup.py"],
                                        part_input_file_path="/1_output.txt", target_num_dict_dir="",
                                        lable_file_dict_dir=""):
        if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name):
            os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name)
        # input_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/output_a.txt"
        input_dir = part_input_file_path
        # output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Api_seq_setup.txt"

        # cg or dfs result
        with open(input_dir, "r") as original_data_file:
            original_data_lines = original_data_file.readlines()
            # self.func_unfold_and_connection_by_file(original_data_lines, target_file_list, min_len)
            # self.func_unfold_and_connection_by_func(original_data_lines, target_file_list, min_len, output_file, proj_name)
            self.func_unfold_and_connection_by_file_target_flexible_funcdef_without_sharp(original_data_lines,
                                                                                          target_file_list, min_len,
                                                                                          output_file_name, proj_name,
                                                                                          folder, target_num_dict_dir,
                                                                                          lable_file_dict_dir)
        # with open(output_dir, "w+") as api_seq_file:
        #     pass


min_len = int(sys.argv[1])
output_file_path = sys.argv[2]
proj_name = sys.argv[3]
folder = sys.argv[4]
method = sys.argv[5]
if sys.argv[6] == "0":
    target_file_list = [""]
else:
    target_file_list = sys.argv[6].split(",")

part_input_file_path = sys.argv[7]
target_num_dict_dir = sys.argv[8]
lable_file_dict_dir = sys.argv[9]
# graph_mode = sys.argv[8]

p = cmd_preprocessor()
p.seq_preprocess_mul_process_main(min_len, output_file_path, proj_name, folder, method, target_file_list,
                                  part_input_file_path, target_num_dict_dir, lable_file_dict_dir)
