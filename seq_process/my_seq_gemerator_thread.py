import concurrent.futures
import os
import pickle
import time

from SourceCode.SequenceGenerator.staticfg.builder import CFGBuilder
from SourceCode.SequenceGenerator.staticfg.staticfg_main import staticfg_main, uncanonical_staticfg_main
from SourceCode.SequenceGenerator.pycg.my_pycg_main import main
from gensim.models import FastText
from gensim.test.utils import datapath
from scipy.spatial.distance import cosine

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This part implements the batch extraction of code behavior sequences from packages to be inspected

# In order to speed up the extraction of the code's behavioral sequences, in this step we only provide behavioral sequence extraction for the two largest .py files in the code package
# of course, you can easily replace this portion of the content to achieve the detection of the entire package.


WE_model_path = datapath("") 
print("start to load our model!")
model = FastText.load(WE_model_path)
print("load model successfully")

with open("", "rb") as sensitive_func_file:
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
        print(f"No py files in {folder_path}, please check!")
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


def process_package(package_path):

    final_files = find_top_2_pyfile(package_path)
    for final_file in final_files:
        path = os.path.basename(final_file)[:-3]
        dst_path = os.path.join(package_path, f"{path}.json")
        print(dst_path)

        ret, output_json, filelist, call_list = generate_cg(final_file, dst_path)
        dfs_out, bfs_out = staticfg_main([final_file], call_list, model, base_vec)
        e_dfs_out_path = os.path.join(package_path, "dfs_out.txt")
        e_bfs_out_path = os.path.join(package_path, "bfs_out.txt")

        with open(e_dfs_out_path, "a") as e_file_dfs, open(e_bfs_out_path, "a") as e_file_bfs:
            e_file_dfs.write(dfs_out)
            e_file_dfs.write("\n")
            e_file_bfs.write(bfs_out)
            e_file_bfs.write("\n")
            print(f"{final_file} done!")


if __name__ == "__main__":
    folder_path = r""

    with concurrent.futures.ThreadPoolExecutor() as executor:
        package_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]
        futures = {}

        for package_path in package_paths:
            if os.path.isfile(os.path.join(package_path, "bfs_out.txt")):
                print(f"Skipping {package_path} because 'bfs_out.txt' already exists.")
            else:
                futures[executor.submit(process_package, package_path)] = package_path

        for future in concurrent.futures.as_completed(futures):
            package_path = futures[future]
            try:
                future.result(timeout=8) 
            except concurrent.futures.TimeoutError:
                print(f"Timeout occurred while processing package {package_path}. Skipping to the next package.")
            except Exception as e:
                print(f"Error processing package {package_path}: {e}")
