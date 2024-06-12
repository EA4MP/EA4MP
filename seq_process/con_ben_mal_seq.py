
# You can mix the extracted malicious code behavior sequences with the benign code behavior sequences after tagging to facilitate the fine-tuning of the BERT model

def merge_text_files(file1_path, file2_path, output_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        file1_content = file1.read()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        file2_content = file2.read()

    merged_content = file1_content + '\n' + file2_content


    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(merged_content)


file1_path = r''
file2_path = r''
output_path = r''

merge_text_files(file1_path, file2_path, output_path)

print("file incorporation finish!")
