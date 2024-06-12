import csv
import filecmp
import json
import pypistats
from pprint import pprint

csv_file_name = r"pac_all_pypi.csv"
with open(csv_file_name, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        pac_name = row[0]
        try:
            data = pypistats.overall(pac_name, mirrors=False, format="json")
            data = json.loads(data)
            downloads = data["data"][0]["downloads"]
            if downloads > 1000:
                print(pac_name)
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
