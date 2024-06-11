import csv
import concurrent.futures
from pathlib import Path
import pypistats
import time  # 导入time模块以使用sleep函数
import json


# 截止到2024-4-8下载量超过100万次的包
# 定义处理每个包下载次数的函数
def process_package(pac_name):
    try:
        data = pypistats.overall(pac_name, mirrors=True, format="json")
        data = json.loads(data)
        downloads = data["data"][0]["downloads"]
        if downloads > 1000000:
            print(pac_name + ": " + str(downloads) + "   YES!!!!!")
            # 将流行包的包名存储到famous.csv文件中去
            with open(famous_csv_file_name, "a") as famous_file:
                famous_file.write(pac_name + "\n")
        else:
            print(pac_name + ": " + str(downloads))
    except Exception as e:
        print(e)

    # 在函数末尾添加500毫秒的休眠
    time.sleep(0.5)


# CSV文件路径
csv_file_name = r"F:\TrainClassfier\src\pac_all_pypi.csv"
famous_csv_file_name = r"F:\TrainClassfier\src\NBProcess\famous.csv"

# 确保famous.csv文件存在

count_all = 0
# 读取CSV文件并创建线程池
with open(csv_file_name, "r") as file, concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # 由于网站对流量的限制，所以这里只能设置为2，设置为3都会提示Client error “429 too many requests” for url
    # 所以这一步的消耗的时间非常非常久
    reader = csv.reader(file)
    reader = list(reader)
    futures = []
    for row in reader:
        pac_name = row[0]
        # 提交任务到线程池
        future = executor.submit(process_package, pac_name)
        futures.append(future)

# 等待所有任务完成
concurrent.futures.wait(futures)
# 在读取网站数据，时间要求很久，请不要关闭电脑谢谢！！！！！！
