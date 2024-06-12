import random

# This part of the implementation slices the merged set of code behavior sequences into a training set and a testing machine, and the slicing is done in a 1:9 fashion

# Setting random seeds for easy slicing
random.seed(45)


train_lines = []
test_lines = []

with open(r'', 'r', encoding='utf-8') as file:
    lines = file.readlines()

if len(lines) < 10:
    raise ValueError("no more than 10 pack , expand your dataset")
for i in range(0, len(lines), 10):
    test_index = random.randint(0, 9)
    test_line = lines[i + test_index]

    train_lines.extend(lines[i:i + 10])
    train_lines.pop(test_index)

    test_lines.append(test_line)

with open('', 'w', encoding='utf-8') as train_file:
    train_file.writelines(train_lines)

with open('', 'w', encoding='utf-8') as test_file:
    test_file.writelines(test_lines)

file.close()
print("finished!")
train_file.close()
test_file.close()
print("tarin set finsh")
print("test set finsh")
