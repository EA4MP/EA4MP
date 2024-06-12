import json
from datetime import datetime
# same as get_meta_information.py
with open('meta_info.json', 'r') as file:
    data = json.load(file)
file.close()

for version, releases in data['releases'].items():
    # print(f"Version: {version}")
    for release in releases:
        downloads = release['downloads']
        upload_time_str = release['upload_time']
        upload_time = datetime.strptime(upload_time_str, "%Y-%m-%dT%H:%M:%S")
        reference_time = datetime(2024, 3, 11)
        file_size = release['size']
        file_name = release['filename']
        url = release['url']
        print("\tDownloads:", downloads)
        print("\tUpload Time:", upload_time_str)
        print("\tURL:", url)
        print("\tfilename", file_name)
        print("\tfilesize", round(file_size/1024/1024, 2), "mb")
