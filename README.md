# EA4MP
## An ensemble approach that integrates deep code behaviors with metadata features for malicious PyPI package detection

You can reproduce our tool according to the following steps：

Before you choose to reproduce our tool, you must first prepare the following: 
(1) Prepare the training set, which consists of malicious and benign packages. 

About malicious packages: 
you can easily get the malicious packages you need from the open source addresses published in the following papers.
a.Backstabber’s Knife Collection: A Review of Open Source Software Supply Chain Attacks
b.World of Code: An Infrastructure for Mining the Universe of Open Source VCS Data
c.Towards Measuring Supply Chain Attacks on Package Managers for Interpreted Languages
d.An Empirical Study of Malicious Code In PyPI Ecosystem
Among them, article (d) publishes the largest known dataset of malicious packets, which already includes more than 5,000+ malicious packets, and you can easily access them.

About benign packages: 
You can randomly download benign packages from pypi, and as a rule, we make packages that have been hosted for more than 90 days and have more than 1,000 downloads benign. The number of downloads and hosting duration can be easily retrieved from the package's json file, which we've posted in a.py file

(2) A word embedding model based on the fasttext model.

1. Code behavior sequence generation and BERT model fine-tuning:


2. Metadata Feature Extraction and ML Model Training


3. Model Ensembling



