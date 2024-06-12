from check_similarity import calculate_similarity
from con_ben_mal_seq import output_path
from get_file_size import get_file_size
from str_2_json import metadata_to_json
import os
import re
import json

author_list = []
with open(r"author_set.txt", "r") as f:
    for line in f:
        author_list.append(line.strip())

popular_packages = []
with open(r"famous.csv", "r") as f:
    for line in f:
        popular_packages.append(line.strip())


def extract_package_name(package_name):
    pattern = r'^([a-zA-Z0-9_-]+?)-\d+(\.\d+)*$'
    match = re.match(pattern, package_name)
    if match:
        return match.group(1)
    else:
        return None


pac_path = r""
for file_name in os.listdir(pac_path):

    if os.path.isdir(os.path.join(pac_path, file_name)):
        print(file_name)
        feature_list = []

        if get_file_size(os.path.join(pac_path, file_name)):
            size_result = get_file_size(os.path.join(pac_path, file_name))
            feature_list.append(size_result - 1)


        with open(os.path.join(pac_path, file_name, "PKG-INFO"), "r", encoding="utf-8") as f:
            metadata_text = f.read()
        json_data = metadata_to_json(metadata_text)
        try:
            json_file = json.loads(json_data)
            if "Name" in json_file:
                pac_name = json_file["Name"]
            else:
                pac_name = extract_package_name(file_name)
        except Exception as e:
            print(e)
        similarity_result = calculate_similarity(popular_packages, pac_name)
        feature_list.append(similarity_result)

        try:
            json_file = json.loads(json_data)
            if "Author" in json_file:
                author = json_file["Author"]
                print(author)
            else:
                author = "UNKNOWN"
        except Exception as e:
            print(e)
        if author in author_list:
            author_flag = 0
            feature_list.append(author_flag)
        elif author == "UNKNOWN":
            author_flag = 1
            feature_list.append(author_flag)
        elif author == "test" or author == "Test" or author == "TEST":
            author_flag = 2
            feature_list.append(author_flag)
        else:
            author_flag = 3
            feature_list.append(author_flag)

        try:
            json_file = json.loads(json_data)
            if "Metadata-Version" in json_file:
                Metadata_Version = json_file["Metadata-Version"]
                print(Metadata_Version)
            else:
                Metadata_Version = "UNKNOWN"
        except Exception as e:
            print(e)
        if Metadata_Version == "UNKNOWN":
            Metadata_Version_flag = 0
            feature_list.append(Metadata_Version_flag)
        else:
            first_digit = int(re.sub(r'\D', '', Metadata_Version.split('.')[0]))
            if first_digit <= 1:
                Metadata_Version_flag = 1
                feature_list.append(Metadata_Version_flag)
            elif 1 < first_digit <= 20:
                Metadata_Version_flag = 2
                feature_list.append(Metadata_Version_flag)
            else:
                Metadata_Version_flag = 3
                feature_list.append(Metadata_Version_flag)

        try:
            json_file = json.loads(json_data)
            if "Version" in json_file:
                Version = json_file["Version"]
                # print(Version)
            else:
                Version = "UNKNOWN"
        except Exception as e:
            print(e)
        if Version == "UNKNOWN":
            Version_flag = 0
            feature_list.append(Version_flag)
        else:
            # result = re.sub(r'\D', '', string)
            first_digit = int(re.sub(r'\D', '', Version.split('.')[0]))
            # int(Version.split('.')[0])
            if first_digit <= 1:
                Version_flag = 1
                feature_list.append(Version_flag)
            elif 1 < first_digit <= 20:
                Version_flag = 2
                feature_list.append(Version_flag)
            else:
                Version_flag = 3
                feature_list.append(Version_flag)
        try:
            json_file = json.loads(json_data)
            if "Home-page" in json_file:
                Home_page = json_file["Home-page"]
                # print(Version)
            else:
                Home_page = "UNKNOWN"
        except Exception as e:
            print(e)
        if Home_page == "UNKNOWN":
            Home_page_flag = 0
            feature_list.append(Home_page_flag)
        else:
            Home_page_flag = 1
            feature_list.append(Home_page_flag)
        try:
            json_file = json.loads(json_data)
            if "Summary" in json_file:
                Summary = json_file["Summary"]
            else:
                Summary = "UNKNOWN"
        except Exception as e:
            print(e)
        words = Summary.split(" ")
        Summary_flag = 0
        if Summary == "UNKNOWN":
            feature_list.append(Summary_flag)
        else:
            Summary_flag = 1
            for word in words:
                if len(word) > 15:
                    Summary_flag = 2
            feature_list.append(Summary_flag)
        try:
            json_file = json.loads(json_data)
            if "Author-email" in json_file:
                Author_email = json_file["Author-email"]
            else:
                Author_email = "UNKNOWN"
        except Exception as e:
            print(e)
        if Author_email == "UNKNOWN":
            Author_email_flag = 0
            feature_list.append(Author_email_flag)
        else:
            Author_email_flag = 1
            feature_list.append(Author_email_flag)
        try:
            json_file = json.loads(json_data)
            if "License" in json_file:
                License = json_file["License"]
            else:
                License = "UNKNOWN"
        except Exception as e:
            print(e)
        if License == "UNKNOWN":
            License_flag = 0
            feature_list.append(License_flag)
        else:
            License_flag = 1
            feature_list.append(License_flag)
        try:
            json_file = json.loads(json_data)
            if "Description" in json_file:
                Description = json_file["Description"]
            else:
                Description = "UNKNOWN"
        except Exception as e:
            print(e)

        if Description == "UNKNOWN":
            Description_flag = 0
            feature_list.append(Description_flag)
        else:
            Description_flag = 1
            feature_list.append(Description_flag)

        mal_ben_flag = 0
        feature_list.append(mal_ben_flag)
        with open("ben-feature.txt", 'a', encoding='utf-8') as f:
            f.write(str(feature_list) + '\n')
        print(feature_list)


