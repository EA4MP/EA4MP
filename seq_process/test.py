# # gxa 2024.3
import os
# def scan_file(path_dir):
#     filenames = tuple([os.path.join(path_dir, f) for f in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))])
#     # for filename in filenames:
#     #     print(filename)
#     return filenames
#
#
# pyfile_dir = "/home/banxiangao/Desktop/MPHunter-main/DataShare/Packages/pyfile"
# pyfile_names = scan_file(pyfile_dir)
# print(pyfile_names[34499])
import time

from gensim.models import FastText
from gensim.test.utils import datapath

# corpus_file = datapath("/home/banxiangao/Desktop/MPHunter-main/test/output_simplified.txt")
#
# model = FastText(vector_size=300, window=5, min_count=1, epochs=15, sg=1, workers=12)
# total_words = model.corpus_total_words
# print(total_words)
# model.build_vocab(corpus_file=corpus_file)
# print("***************")
# total_words = model.corpus_total_words
# print(total_words)
# print("start training")
# model.train(corpus_file=corpus_file,total_words=total_words,epochs=15)
# print("start saving")
# model.save("/home/banxiangao/Desktop/MPHunter-main/test/my_model")

# model = FastText.load("/home/banxiangao/Desktop/MPHunter-main/test/my_model")
# print("LOAD MODEL SUCCESSFULLY !")
# count = 0
# with open("/home/banxiangao/Desktop/MPHunter-main/test/output_simplified.txt", "rb") as fp:
#     api_seqs = fp.readlines()
#     print(len(api_seqs))
#     # time.sleep(3000)
#     for api_seq in api_seqs:
#         count += 1
#         word_vector = model.wv.word_vec(api_seq)
#         print(f"**************{count}****************")
#         print(word_vector)
#         vec_str = "\n".join(map(str, word_vector))
#         with open("/home/banxiangao/Desktop/MPHunter-main/test/vec.txt", "a") as get_vec:
#             get_vec.write(vec_str)
#             get_vec.write("\n")
#         get_vec.close()
# fp.close()

# with open("/home/banxiangao/Desktop/MPHunter-main/test/output_simplified.txt", "rb") as api_seqs:
#     for api_seq in api_seqs:
#         print(api_seq)

