import csv
import concurrent.futures
from pathlib import Path
import pypistats
import time 
import json



def process_package(pac_name):
    try:
        data = pypistats.overall(pac_name, mirrors=True, format="json")
        data = json.loads(data)
        downloads = data["data"][0]["downloads"]
        if downloads > 1000:
            print(pac_name + ": " + str(downloads) + "   YES!!!!!")
            with open(famous_csv_file_name, "a") as famous_file:
                famous_file.write(pac_name + "\n")
        else:
            print(pac_name + ": " + str(downloads))
    except Exception as e:
        print(e)

    time.sleep(0.5)


csv_file_name = r"pac_all_pypi.csv"
famous_csv_file_name = r"famous.csv"


count_all = 0

with open(csv_file_name, "r") as file, concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

    reader = csv.reader(file)
    reader = list(reader)
    futures = []
    for row in reader:
        pac_name = row[0]

        future = executor.submit(process_package, pac_name)
        futures.append(future)
concurrent.futures.wait(futures)
