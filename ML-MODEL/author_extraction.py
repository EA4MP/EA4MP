
import os
import json
from str_2_json import metadata_to_json


pac_path = r""
license_list = ['MIT', 'Eclipse', 'Apache', 'ZPL', 'apache2', 'BSD', 'MPL-2.0', 'APACHE', 'license', 'LICENSE.txt', 'GPLv3', 'GNU', 'gpl-3.0.txt', 'GPL', 'New', 'Dual', 'Copyright', 'Apache-2.0', 'request', 'SentinelOne']
for file_name in os.listdir(pac_path):
    if os.path.isdir(os.path.join(pac_path, file_name)):
        try:
            with open(os.path.join(pac_path, file_name, "PKG-INFO"), "r", encoding="utf-8") as f:
                metadata_text = f.read()
            json_data = metadata_to_json(metadata_text)
            try:
                json_file = json.loads(json_data)
                if "License" in json_file:
                    License = json_file["License"].split(" ")[0]
                else:
                    License = "UNKNOWN"
            except Exception as e:
                print(e)
            if License not in license_list:
                license_list.append(License)
                print(License)
        except Exception as e:
            print(e)


print(license_list)
