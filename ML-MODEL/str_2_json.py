import json
import chardet


def metadata_to_json(metadata_text):
    metadata_lines = [line.strip() for line in metadata_text.strip().split("\n")]


    metadata = {}


    key = None
    value = ""


    for line in metadata_lines:

        if line.startswith(" "):

            value += " " + line.strip()
        else:

            if key is not None:
                metadata[key] = value.strip()

                if key == "Description":
                    value += " " + line.strip()

            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
            else:

                continue

    if key is not None:
        metadata[key] = value.strip()

    json_data = json.dumps(metadata, indent=4)

    return json_data


with open("PKG-INFO", "r", encoding="utf-8") as f:
    metadata_text = f.read()
# detected_encoding = chardet.detect(metadata_text)['encoding']
# print(detected_encoding)
json_data = metadata_to_json(metadata_text)
# json_file = json.loads(json_data)

try:
    json_file = json.loads(json_data)
    if "Metadata-Version" in json_file:
        print(json_file["Metadata-Version"])
    else:
        print("no Metadata-Version")
except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format {e}")
