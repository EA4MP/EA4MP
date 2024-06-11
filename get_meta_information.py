import requests
import os
import json
from datetime import datetime
import csv

count_2020 = 0
count_2021 = 0
count_2022 = 0
count_2023 = 0

count_pac_2020 = 0
count_pac_2021 = 0
count_pac_2022 = 0
count_pac_2023 = 0
csv_file_name = r"F:\TrainClassfier\src\pac_all_pypi.csv"
with open(csv_file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        package_name = row[0]
        # print(package_name)
        try:
            flag_2020 = False
            flag_2021 = False
            flag_2022 = False
            flag_2023 = False
            response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
            data = response.json()
            for version, releases in data['releases'].items():
                # print(f"Version: {version}")
                for release in releases:
                    upload_time_str = release['upload_time']
                    upload_time = datetime.strptime(upload_time_str, "%Y-%m-%dT%H:%M:%S")
                    if upload_time < datetime(2021, 1, 1):
                        flag_2020 = True
                        count_pac_2020 += 1
                    if upload_time < datetime(2022, 1, 1):
                        flag_2021 = True
                        count_pac_2021 += 1
                    if upload_time < datetime(2023, 1, 1):
                        flag_2022 = True
                        count_pac_2022 += 1
                    if upload_time < datetime(2024, 1, 1):
                        flag_2023 = True
                        count_pac_2023 += 1
                    if upload_time > datetime(2024, 3, 29):
                        url = release['url']
                        file_size = release['size']
                        file_name = release['filename']
                        if file_name.endswith('.tar.gz'):
                            print(file_name)
                            print(url)
                            print(file_size)
                            print("**********************")
                if flag_2020:
                    count_2020 += 1
                if flag_2021:
                    count_2021 += 1
                if flag_2022:
                    count_2022 += 1
                if flag_2023:
                    count_2023 += 1
        except Exception as e:
            print(f"get {package_name} update information wrong since {e}")


print(f"2020: {count_2020}, 2021: {count_2021}, 2022: {count_2022}, 2023: {count_2023}")
print(f"2020: {count_pac_2020}, 2021: {count_pac_2021}, 2022: {count_pac_2022}, 2023: {count_pac_2023}")
# response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
# pac_file = "meta4_info.json"
# data = response.json()
# print(data)
# for version, releases in data['releases'].items():
#     # print(f"Version: {version}")
#     for release in releases:
#         downloads = release['downloads']
#         upload_time_str = release['upload_time']
#         upload_time = datetime.strptime(upload_time_str, "%Y-%m-%dT%H:%M:%S")
#         reference_time = datetime(2024, 3, 11)
#         file_size = release['size']
#         file_name = release['filename']
#         url = release['url']
#         print("\tDownloads:", downloads)
#         print("\tUpload Time:", upload_time_str)
#         print("\tURL:", url)
#         print("\tfilename", file_name)
#         print("\tfilesize", round(file_size/1024/1024, 2), "mb")
# 'https://pypi.org/pypi//json'