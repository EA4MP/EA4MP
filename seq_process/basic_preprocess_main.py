import os, pickle, gc, shutil
import sys, subprocess
from func_timeout import func_set_timeout
from multiprocessing import Pool
import re

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(PROJECT_DIR)


class Preprocessor:
    def __init__(self):
        self.path_sign = 1
        self.content_sign = 0
        self.target_sign = 0
        self.current_file = ""
        self.output_content = ""
        self.target_dict = {}   # target label: target count
        self.label_file_dict = {}   # label : file name
        self.target_count = 0
        self.funcdef_list = []

    def func_unfold_and_connection_by_file(self, original_data_lines, target_list=[], min_len=0,
                                           output_file_name="output_connected.txt", proj_name="test",
                                           folder="WordEmbedding"):
        dict, funcdef_call_count_dict = self.prepare_dict(original_data_lines)

        # output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/output_a_c.txt"
        output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + \
                     "/" + output_file_name
        with open(output_dir, "w+") as output:
            i = 0
            for original_data_line in original_data_lines:
                # print("line: " + original_data_line)
                if original_data_line.strip() == "":
                    if self.content_sign == 1 and self.path_sign == 0:
                        if self.output_content.strip() != "":
                            if len(self.output_content.strip().split()) >= min_len:
                                i = i + 1
                                # print("output")
                                output.write(self.output_content.strip() + "\n")     # add label in here
                                if self.target_sign == 1:
                                    self.target_count += 1
                                    self.target_dict[self.target_count] = i
                                    self.label_file_dict[self.target_count] = self.current_file
                        self.content_sign = 0
                        self.target_sign = 0
                        self.path_sign = 1
                        # print("end")
                        # end of a seq
                    if self.path_sign == 1 and self.content_sign == 0:
                        self.content_sign = 1
                        self.output_content = ""
                        # print("start")
                        # start of a seq
                    elif self.path_sign == 0 and self.content_sign == 0:
                        self.content_sign = 1
                    continue
                if original_data_line[0] == '/':
                    if target_list == [] or original_data_line.split("/")[-1].strip() in target_list:
                        # print("bingo")
                        self.target_sign = 1
                    self.path_sign = 0
                    self.content_sign = 0
                    self.current_file = original_data_line
                    # self.output_content += "\n" + original_data_line.strip()
                    continue
                else:
                    # print(1)
                    sign = 0
                    for word in original_data_line.split(" "):
                        if word.strip() == "" or word[0] == "(":
                            continue
                        if sign == 1 and word[-1] != "]":
                            continue
                        elif sign == 1 and word[-1] == "]":
                            sign = 0
                            continue
                        if word[0:6] == "<call>":
                            # print("call:" + word)
                            if self.target_sign == 1:
                                # print(word)
                                self.output_content += self.find_seq(word[6:], "", dict, [], 0)
                            else:
                                self.output_content += word.split(".")[-1].strip() + "# "
                            # print(self.find_seq(word[6:], "", dict, [], 0))
                        elif word[0] == "[":
                            if word[1:7] == "<call>":
                                # call序列
                                if self.target_sign == 1:
                                    self.output_content += self.find_seq(word[6:], "", dict, [], 0)
                                else:
                                    self.output_content += word.split(".")[-1].strip() + "# "
                            else:
                                self.output_content += word[1:] + " "
                            sign = 1
                        else:
                            self.output_content += word.strip() + " "
                    self.path_sign = 0
                    self.content_sign = 1
        target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict.pkl"
        # target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict_temp.pkl"
        with open(target_num_dict_dir, "wb+") as file:
            pickle.dump(self.target_dict, file)
        target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/label_file_dict.pkl"
        with open(target_num_dict_dir, "wb+") as file:
            pickle.dump(self.label_file_dict, file)

    def func_unfold_and_connection_by_func(self, original_data_lines, target_list=[], min_len=0,
                                           input_filename="output_connected.txt", proj_name="test",
                                           folder="WordEmbedding"):
        # function call will be attached with a "#"

        dict, funcdef_call_count_dict = self.prepare_dict(original_data_lines)

        output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + \
                     input_filename
        with open(output_dir, "w+") as output:
            i = 0
            for original_data_line in original_data_lines:
                # print("line: " + original_data_line)
                if original_data_line.strip() == "":
                    if self.path_sign == 0 and self.content_sign == 1:
                        if self.output_content.strip() != "":
                            if len(self.output_content.strip().split()) >= min_len:
                                if self.target_sign == 1:
                                    i = i + 1
                                    output.write(self.output_content.strip() + "\n")  # add label in here
                                    output.flush()
                                    self.target_count += 1
                                    self.target_dict[self.target_count] = i
                                    self.label_file_dict[self.target_count] = self.current_file
                        self.content_sign = 0
                        self.target_sign = 0
                        self.path_sign = 1
                        gc.collect(2)
                        # end of a seq
                    if self.path_sign == 1 and self.content_sign == 0:
                        self.content_sign = 1
                        self.output_content = ""
                        # start of a seq
                    elif self.path_sign == 0 and self.content_sign == 0:
                        self.content_sign = 1
                    continue
                if original_data_line[0] == '/':
                    if target_list == [] or original_data_line.split("/")[-1].strip() in target_list:
                        self.target_sign = 1
                    self.path_sign = 0
                    self.content_sign = 0
                    self.current_file = original_data_line
                    continue
                else:
                    sign = 0
                    func_sign = 0
                    for word in original_data_line.split(" "):
                        if word.strip() == "" or word[0] == "(":
                            func_sign = 1
                            continue
                        if sign == 1 and word[-1] != "]":
                            continue
                        elif sign == 1 and word[-1] == "]":
                            sign = 0
                            continue
                        if word[0:6] == "<call>":
                            # print("call:" + word)
                            if self.target_sign == 1:
                                self.output_content += self.find_seq(word[6:], "", dict, [], 0)
                            else:
                                self.output_content += word.split(".")[-1].strip() + "# "
                            # print(self.find_seq(word[6:], "", dict, [], 0))
                        elif word[0] == "[":
                            if word[1:7] == "<call>":
                                # call序列
                                if self.target_sign == 1:
                                    self.output_content += self.find_seq(word[6:], "", dict, [], 0)
                                else:
                                    self.output_content += word.split(".")[-1].strip() + "# "
                            else:
                                self.output_content += word[1:] + " "
                            sign = 1
                        else:
                            self.output_content += word.strip() + " "

                    if self.target_sign != 1 and func_sign == 1 and self.output_content.strip() != "":
                        i = i + 1
                        output.write(self.output_content.strip() + "\n")  # add label in here
                        self.output_content = ""
                    self.path_sign = 0
                    self.content_sign = 1

        target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict.pkl"
        # target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict_temp.pkl"
        with open(target_num_dict_dir, "wb+") as file:
            pickle.dump(self.target_dict, file)
        target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/label_file_dict.pkl"
        with open(target_num_dict_dir, "wb+") as file:
            pickle.dump(self.label_file_dict, file)

    def func_unfold_and_connection_by_func_target_without_funcdef(self, original_data_lines, target_list=[], min_len=0, input_filename="output_connected.txt", proj_name="test", folder="WordEmbedding"):
        dict, funcdef_call_count_dict = self.prepare_dict(original_data_lines)
        output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + input_filename
        with open(output_dir, "w+") as output:
            i = 0
            for original_data_line in original_data_lines:
                # print("line: " + original_data_line)
                if original_data_line.strip() == "":
                    if self.path_sign == 0 and self.content_sign == 1:
                        if self.output_content.strip() != "":
                            if len(self.output_content.strip().split()) >= min_len:
                                if self.target_sign == 1:
                                    i = i + 1
                                    output.write(self.output_content.strip() + "\n")  # add label in here
                                    output.flush()
                                    self.target_count += 1
                                    self.target_dict[self.target_count] = i
                                    self.label_file_dict[self.target_count] = self.current_file
                        self.content_sign = 0
                        self.target_sign = 0
                        self.path_sign = 1
                        gc.collect(2)
                        # end of a seq
                    if self.path_sign == 1 and self.content_sign == 0:
                        self.content_sign = 1
                        self.output_content = ""
                        # start of a seq
                    elif self.path_sign == 0 and self.content_sign == 0:
                        self.content_sign = 1
                    continue
                if original_data_line[0] == '/':
                    #路径行
                    if target_list == [] or original_data_line.split("/")[-1].strip() in target_list:
                        self.target_sign = 1
                    self.path_sign = 0
                    self.content_sign = 0
                    self.current_file = original_data_line
                    continue
                else:
                    # 非路径的内容行
                    sign = 0
                    func_sign = 0
                    for word in original_data_line.split(" "):
                        if word.strip() == "" or word[0] == "(":
                            func_sign = 1
                            if self.target_sign == 1:
                                break
                            else:
                                continue
                        if sign == 1 and word[-1] != "]":
                            continue
                        elif sign == 1 and word[-1] == "]":
                            sign = 0
                            continue
                        if word[0:6] == "<call>":
                            # call序列
                            # print("call:" + word)
                            if self.target_sign == 1:
                                self.output_content += self.find_seq(word[6:], "", dict, [], 0)
                            else:
                                self.output_content += word.split(".")[-1].strip() + "# "
                            # print(self.find_seq(word[6:], "", dict, [], 0))
                        elif word[0] == "[":
                            if word[1:7] == "<call>":
                                # call序列
                                if self.target_sign == 1:
                                    self.output_content += self.find_seq(word[6:], "", dict, [], 0)
                                else:
                                    self.output_content += word.split(".")[-1].strip() + "# "
                            else:
                                self.output_content += word[1:] + " "
                            sign = 1
                        else:
                            self.output_content += word.strip() + " "

                    if self.target_sign != 1 and func_sign == 1 and self.output_content.strip() != "":
                        i = i + 1
                        output.write(self.output_content.strip() + "\n")  # add label in here
                        self.output_content = ""
                    self.path_sign = 0
                    self.content_sign = 1

        target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict.pkl"
        # target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict_temp.pkl"
        with open(target_num_dict_dir, "wb+") as file:
            pickle.dump(self.target_dict, file)
        target_num_dict_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/label_file_dict.pkl"
        with open(target_num_dict_dir, "wb+") as file:
            pickle.dump(self.label_file_dict, file)

    def func_unfold_and_connection_by_file_target_flexible_funcdef_without_sharp\
                    (self, original_data_lines, target_list=[], min_len=0, output_file_path="output_connected.txt",
                     proj_name="test", folder="WordEmbedding", target_num_dict_dir="", lable_file_dict_dir=""):
        funcdef_content_dict, funcdef_call_count_dict = self.prepare_dict(original_data_lines)

        # output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/output_a_c.txt"
        # output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + output_file_name
        output_dir = output_file_path
        with open(output_dir, "w+") as output:
            i = 0
            for original_data_line in original_data_lines:
                # print("line: " + original_data_line)
                if original_data_line.strip() == "":
                    if self.content_sign == 1 and self.path_sign == 0:
                        # if a function define wasn't called explicitly,
                        # then we will attach its line at the end of the seq.
                        for funcdef in self.funcdef_list:
                            if funcdef_call_count_dict[funcdef] == 0:
                                self.process_content_line(" ".join(funcdef_content_dict[funcdef]), funcdef_call_count_dict, funcdef_content_dict)
                        if self.output_content.strip() != "":
                            if len(self.output_content.strip().split()) >= min_len:
                                i = i + 1
                                # print("output")
                                output.write(self.output_content.strip() + "\n")     # add label in here
                                if self.target_sign == 1:
                                    self.target_count += 1
                                    self.target_dict[self.target_count] = i
                                    self.label_file_dict[self.target_count] = self.current_file
                        self.content_sign = 0
                        self.target_sign = 0
                        self.path_sign = 1
                        self.funcdef_list = []
                        # print("end")
                        # end of a seq
                    if self.path_sign == 1 and self.content_sign == 0:
                        self.content_sign = 1
                        self.output_content = ""
                        # print("start")
                        # start of a seq
                    elif self.path_sign == 0 and self.content_sign == 0:
                        # this is a content line, but it is empty
                        self.content_sign = 1
                    continue
                if original_data_line[0] == '/':
                    if target_list == [] or original_data_line.split("/")[-1].strip() in target_list:
                        # print("bingo")
                        self.target_sign = 1
                        # print(original_data_line)
                    self.path_sign = 0
                    self.content_sign = 0
                    self.current_file = original_data_line
                    # self.output_content += "\n" + original_data_line.strip()
                    continue
                else:
                    # print(1)
                    self.process_content_line(original_data_line, funcdef_call_count_dict, funcdef_content_dict)
                    self.path_sign = 0
                    self.content_sign = 1
        with open(target_num_dict_dir, "wb+") as file:
            pickle.dump(self.target_dict, file)
        with open(lable_file_dict_dir, "wb+") as file:
            pickle.dump(self.label_file_dict, file)

    def process_content_line(self, original_data_line, funcdef_call_count_dict, funcdef_content_dict):
        sign = 0
        for word in original_data_line.split(" "):
            if word.strip() == "":
                continue
            if word[0] == "(":
                self.funcdef_list.append(word[1:-2])
                break
            if sign == 1 and word[-1] != "]":
                continue
            elif sign == 1 and word[-1] == "]":
                sign = 0
                continue
            if word[0:6] == "<call>":
                # print("call:" + word)
                if self.target_sign == 1:
                    # print(word)
                    self.output_content += self.find_seq(word[6:], "", funcdef_content_dict, [], 0)
                    if word[6:] in funcdef_call_count_dict.keys():
                        funcdef_call_count_dict[word[6:]] += 1
                else:
                    self.output_content += word.split(".")[-1].strip() + " "
                    if word[6:] in funcdef_call_count_dict.keys():
                        funcdef_call_count_dict[word[6:]] += 1
                # print(self.find_seq(word[6:], "", funcdef_content_dict, [], 0))
            elif word[0] == "[":
                if word[1:7] == "<call>":
                    # call序列
                    if self.target_sign == 1:
                        self.output_content += self.find_seq(word[7:], "", funcdef_content_dict, [], 0)
                        if word[7:] in funcdef_call_count_dict.keys():
                            funcdef_call_count_dict[word[7:]] += 1
                    else:
                        self.output_content += word.split(".")[-1].strip() + " "
                        if word[7:] in funcdef_call_count_dict.keys():
                            funcdef_call_count_dict[word[7:]] += 1
                else:
                    self.output_content += word[1:] + " "
                sign = 1
            else:
                self.output_content += word.strip() + " "

    def find_seq(self, key, output, funcdef_content_dict, visited, deepth):
        if key in visited:
            return key.split(".")[-1]
        visited.append(key)
        deepth += 1

        if deepth > 1:
            # print(key)
            return ""
        try:
            value = funcdef_content_dict[key]
        except:
            return ""

        sign = 0
        for word in value:
            if len(word) > 6 and word[0:6] == "<call>":
                output += self.find_seq(word[6:], output, funcdef_content_dict, visited, deepth)
                # print(sys.getsizeof(self.find_seq)/1024/1024)
                continue
            if sign == 1 and word[-1] != "]":
                continue
            elif sign == 1 and word[-1] == "]":
                sign = 0
            elif word[0] == "[":
                output += word[1:] + " "
                sign = 1
            else:
                output += word.strip() + " "
        del visited, value, funcdef_content_dict
        gc.collect(2)
        return output

    def prepare_dict(self, original_data_lines):
        # prepare dict : funcdef name ==> funcdef content   and   funcdef name ==> funcdef call number
        # result_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/funcdef_dict_temp.pkl"
        result_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/funcdef_dict.pkl"
        result_dir2 = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/funcdef_call_counter_dict.pkl"
        funcdef_content_dict ={}
        call_counter_dict = {}
        for line in original_data_lines:
            if line[0] == "(":
                # print(" ".join(line.split(" ")[1:-1]))
                funcdef_name = line.split(" ")[0][1:-2]
                funcdef_content_dict[funcdef_name] = line.strip().split(" ")[1:]
                call_counter_dict[funcdef_name] = 0
        with open(result_dir, "wb+") as file:
            pickle.dump(funcdef_content_dict, file)
        with open(result_dir2, "wb+") as file:
            pickle.dump(call_counter_dict, file)
        return funcdef_content_dict, call_counter_dict

    def seq_preprocess_setup_dfs_only(self, min_len=0, output_file="output_connected.txt", proj_name="test", folder="WordEmbedding", method="ft"):
        if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name):
            os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name)
        # input_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/output_a.txt"
        input_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/output.txt"
        # output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Api_seq_setup.txt"

        with open(input_dir, "r") as original_data_file:
            original_data_lines = original_data_file.readlines()
            # self.func_unfold_and_connection_by_file(original_data_lines, ["setup.py"], min_len)
            # self.func_unfold_and_connection_by_func(original_data_lines, ["setup.py"], min_len, output_file, proj_name)
            self.func_unfold_and_connection_by_file_target_flexible_funcdef_without_sharp(original_data_lines,
                                                                ["setup.py"], min_len, output_file, proj_name, folder)
        # with open(output_dir, "w+") as api_seq_file:
        #     pass
        shutil.copytree(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/PreProcess")
        shutil.copyfile(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict.pkl", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + proj_name + "_" + method + "_target_num_dict.pkl")
        shutil.copyfile(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/label_file_dict.pkl", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + proj_name + "_" + method + "_label_file_dict.pkl")

    def seq_preprocess(self, min_len=0, output_file="output_connected.txt", proj_name="test", folder="WordEmbedding",
                       method="ft", target_file_list=["setup.py"], ifbfs=True, input_file="output.txt"):
        if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name):
            os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name)
        # input_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/output_a.txt"
        input_dir_dfs = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + input_file
        input_dir_bfs = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/bfs_output.txt"
        # output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Api_seq_setup.txt"

        # dfs result
        with open(input_dir_dfs, "r") as original_data_file:
            original_data_lines = original_data_file.readlines()
            # self.func_unfold_and_connection_by_file(original_data_lines, target_file_list, min_len)
            # self.func_unfold_and_connection_by_func(original_data_lines, target_file_list, min_len, output_file, proj_name)
            self.func_unfold_and_connection_by_file_target_flexible_funcdef_without_sharp(original_data_lines,
                                                                target_file_list, min_len, output_file, proj_name, folder)
        # with open(output_dir, "w+") as api_seq_file:
        #     pass
        shutil.copytree(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/PreProcess")
        shutil.copyfile(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict.pkl", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + proj_name + "_" + method + "_target_num_dict.pkl")
        shutil.copyfile(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/label_file_dict.pkl", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + proj_name + "_" + method + "_label_file_dict.pkl")

        if ifbfs:
            with open(input_dir_bfs, "r") as original_data_file:
                original_data_lines = original_data_file.readlines()
                # self.func_unfold_and_connection_by_file(original_data_lines, target_file_list, min_len)
                # self.func_unfold_and_connection_by_func(original_data_lines, target_file_list, min_len, output_file, proj_name)
                self.func_unfold_and_connection_by_file_target_flexible_funcdef_without_sharp(original_data_lines,
                                                                    target_file_list, min_len, "bfs_" + output_file, proj_name, folder)
        # with open(output_dir, "w+") as api_seq_file:
        #     pass

    def seq_preprocess_noexpansion(self, output_file="output_connected.txt", proj_name="test", folder="WordEmbedding", method="ft"):
        if not os.path.exists(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name):
            os.mkdir(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name)
        input_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/output.txt"
        # output_dir = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Api_seq_noexpansion.txt"

        with open(input_dir, "r") as original_data_file:
            original_data_lines = original_data_file.readlines()
        sys.getsizeof(original_data_lines)
        # self.func_unfold_and_connection_by_file(original_data_lines, [], min_len=4)
        self.func_unfold_and_connection_by_func(original_data_lines, [], 4, output_file, proj_name, folder)

        # with open(output_dir, "w+") as api_seq_file:
        #     pass
        shutil.copytree(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/PreProcess")
        shutil.copyfile(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/target_num_dict.pkl", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + proj_name + "_" + method + "_target_num_dict.pkl")
        shutil.copyfile(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess/label_file_dict.pkl", PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + proj_name + "_" + method + "_label_file_dict.pkl")

    def do_cmd(self, cmd):
        p = subprocess.Popen(cmd, shell=True)
        print("wait")
        p.wait()
        p.kill()

    def seq_preprocess_mul_process(self, min_len=0, output_file_name="output_connected.txt", proj_name="test",
                                   folder="WordEmbedding", method="ft", target_file_list=["setup.py"],
                                   graph_mode="cfg+cg", task_num=20):
        # 多线程的API调用序列生成，被主程序采用。
        if graph_mode == "cfg+cg":
            for_mul_process_folder_path = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + \
                                          folder + "/" + proj_name + "/ForMulProcess_cfg"
            prefixes = ["dfs_", "bfs_"]
        elif graph_mode == "cg":
            for_mul_process_folder_path = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + \
                                          folder + "/" + proj_name + "/ForMulProcess"
            prefixes = ["cg_"]

        output_file_list = os.listdir(for_mul_process_folder_path)
        cmd_list = []
        for prefix in prefixes:
            id_list = sorted(list(filter(lambda x: re.match(".*" + prefix + "output.txt", x) != None, output_file_list)))
            print(id_list)
            for id in id_list:
                id = str(id).split("_")[0]
                input_file_path = for_mul_process_folder_path + "/" + id + "_" + prefix + "output.txt"
                output_file_path = for_mul_process_folder_path + "/" + id + "_" + prefix + "connected_output.txt"
                target_num_dict_dir = for_mul_process_folder_path + "/" + id + "_" + prefix + "target_num_dict.pkl"
                lable_file_dict_dir = for_mul_process_folder_path + "/" + id + "_" + prefix + "label_file_dict.pkl"
                if target_file_list == [""]:
                    target_file_para = "0"
                else:
                    target_file_para = ",".join(target_file_list)
                arg_list = [str(min_len), output_file_path, proj_name, folder, method, target_file_para,
                            input_file_path, target_num_dict_dir, lable_file_dict_dir]
                long_para = " ".join(arg_list)
                cmd_list.append("python3 " + PROJECT_DIR + "/SequenceGenerator/do_single_process_basic_preprocess.py"
                                + " " + long_para)
        with Pool(task_num) as pool:
            pool.map(self.do_cmd, cmd_list)
        print("inline graph: done")
        output_file_list = os.listdir(for_mul_process_folder_path)
        shutil.copytree(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/PreProcess",
                        PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/PreProcess")
        t_sum_dict = {}
        sum_dict = {}
        for prefix in prefixes[:1]:
            tndf_list = sorted(list(filter(lambda x: re.match(".*" + prefix + "target_num_dict.pkl", x) != None, output_file_list)))
            for tnd_file in tndf_list:
                with open(for_mul_process_folder_path + "/" + tnd_file, "rb") as t_file1:
                    temp_dict1 = pickle.load(t_file1)
                    num = len(t_sum_dict)
                    for k, v in temp_dict1.items():
                        t_sum_dict[k + num] = v
            # print(len(t_sum_dict))

            lfdf_list = sorted(list(filter(lambda x: re.match(".*" + prefix + "label_file_dict.pkl", x) != None, output_file_list)))
            print(lfdf_list)
            for lfd_file in lfdf_list:
                with open(for_mul_process_folder_path + "/" + lfd_file, "rb") as t_file1:
                    temp_dict1 = pickle.load(t_file1)
                    num = len(sum_dict)
                    for k, v in temp_dict1.items():
                        sum_dict[k + num] = v
        with open(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + proj_name + "_" + method + "_label_file_dict.pkl",
                "wb") as l_file3:
            pickle.dump(sum_dict, l_file3)
        with open(PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + "/" + proj_name + "_" + method + "_target_num_dict.pkl",
                "wb") as t_file3:
            pickle.dump(t_sum_dict, t_file3)
        with open(for_mul_process_folder_path + "/../PreProcess/" + proj_name + "_" + method + "_target_num_dict.pkl", "wb") as l_file3:
            pickle.dump(t_sum_dict, l_file3)
        with open(for_mul_process_folder_path + "/../PreProcess/" + proj_name + "_" + method + "_label_file_dict.pkl", "wb") as t_file3:
            pickle.dump(sum_dict, t_file3)


        for prefix in prefixes:
            if prefix == "dfs_":
                output_prefix = ""
            else:
                output_prefix = prefix
            output_file = PROJECT_DIR + "/DataShare/ApiSeq_and_Result/Result/" + folder + "/" + proj_name + \
                          "/" + output_prefix + output_file_name
            cmd = "cd " + for_mul_process_folder_path + "; cat *_" + prefix + "connected_output.txt > " + output_file
            os.system(cmd)


if __name__ == "__main__":
    folder = "SentenceEmbedding"
    proj_name = "0304_900-pkg_malicious_setup_c.x"
    # "0214_12000-pkg_for_corpus_c.x"  or   "0214_6000-pkg_new_updated_pypi_setup_c.x" or "0214_200-pkg_negative_c.x"
    output_file_name = "output_connected_0304_900_c.x.txt"
    method = "ft"

    pre = Preprocessor()
    pre.seq_preprocess(0, output_file_name, proj_name, folder, method)