import random

# In order to reduce the effect of randomness on the results, we perform a disruption operation on the collated sequence

def shuffle_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    random.shuffle(lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)


shuffle_lines(r'file_input.txt', r'file_output.txt')
