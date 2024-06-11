import csv
import filecmp
import json
import pypistats
from pprint import pprint

# 获取每个pypi包的下载次数，并将下载次数超过100000次的软件包作为流行包，作为后续验证是否存在typosquatting的基准
csv_file_name = r"F:\TrainClassfier\src\pac_all_pypi.csv"
with open(csv_file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        pac_name = row[0]
        try:
            data = pypistats.overall(pac_name, mirrors=False, format="json")
            data = json.loads(data)
            downloads = data["data"][0]["downloads"]
            if downloads > 100000:
                print(pac_name)
                # 将流行包的包名存储到famous.csv文件中去
                famous_csv_file_name = r"F:\TrainClassfier\src\NBProcess\famous.csv"
                with open(famous_csv_file_name, "a") as famous_file:
                    famous_file.write(pac_name + "\n")
            else:
                print("not famous!")
            # pprint(downloads)
        except Exception as e:
            print(e)
file.close()
famous_file.close()
