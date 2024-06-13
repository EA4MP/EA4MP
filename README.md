# EA4MP
## An ensemble approach that integrates deep code behaviors with metadata features for malicious PyPI package detection

You can reproduce our tool according to the following steps:

### Preparation
Before you reproduce our tool, you must first prepare the following:

1. **Prepare the Training Set**:
    - **Malicious Packages**: You can get malicious packages from the open-source addresses published in the following papers:
        - Backstabber’s Knife Collection: A Review of Open Source Software Supply Chain Attacks
        - World of Code: An Infrastructure for Mining the Universe of Open Source VCS Data
        - Towards Measuring Supply Chain Attacks on Package Managers for Interpreted Languages
        - An Empirical Study of Malicious Code In PyPI Ecosystem [pypi_malregistry](https://github.com/lxyeternal/pypi_malregistry)
   
    Among them, article (d) publishes the largest known dataset of malicious packets, which includes more than 5,000+ malicious packets.

    - **Benign Packages**: You can randomly download benign packages from PyPI. As a rule, we consider packages hosted for more than 90 days and with more than 1,000 downloads as benign. The number of downloads and hosting duration can be retrieved from `https://pypi.org/pypi/{package_name}/json`, which we've utilized in the `get_meta_information.py` file.

2. **Word Embedding Model**:
    - A word embedding model based on the FastText model. We referenced the methodology used to train the word embedding model in the paper “A Needle is an Outlier in a Haystack: Hunting Malicious PyPI Packages with Code Clustering”. You can find the open-source code of the paper and train the FastText model according to its instructions.
    [MPHunter GitHub Repository](https://github.com/rwnbiad105/MPHunter)

    Since this tool only needs to use the model once to sort the sequence of function calls, you only need to train the first model. If you choose not to sort the function call sequences and generate code behavior sequences directly, we have also implemented this method in the code. You can comment out parts of the code to achieve direct generation of code behavior sequences. (Note: Direct code generation may impact the final results.)

### Steps to Reproduce

1. **Code Behavior Sequence Generation and BERT Model Fine-tuning**:
    - After you have prepared all the data and made the corresponding substitutions to the file addresses in the code, run the following in the `seq_process` folder:
      ```sh
      python my_seq_generator_thread.py
      ```
    The script will automate the code behavior sequence extraction for all your pending packages using a thread pool. To speed up the reproduction, we have simplified the code behavior sequence extraction by identifying the files in the package and scanning only the two largest script files including `setup.py` (we will scan `setup.py` regardless of its size). Through our real-world testing, the sequences extracted this way are sufficient.

   - You can run this script to fine_tuning your own BERT model.
     ```sh
     python fine_tune_with_GPU.py
     ```
    Before you try to fine_tuning the BERT model, you need to download the pre_trained BERT model from [huggingface](https://huggingface.co/google-bert). You can choose the BERT_base or BERT_large.  It's worth noting that fine-tuning the BERT_large model took much longer (over 8 hours of running on a V100, 32GB GPU).

2. **Metadata Feature Extraction and ML Model Training**
    In the `ML-MODEL` folder, we provide methods for extracting metadata feature vectors and training scripts for four major machine learning models. You can follow the provided code, fill in the corresponding file paths, and then execute the following scripts:

    ```sh
    python feature_ex.py
    cd train
    python train_DT_classifier.py
    python train_RF_classifier.py
    python train_NB_classifier.py
    python train_svm_classifier.py
    ```
    The trained models will be automatically saved in the directory you specified.
    Note: For privacy reasons, we have hidden the specific file paths. However, based on the code information, we believe you can easily fill in the required file paths.    
3. **Model Ensembling**

我们在Ensemble文件夹下提供了两种不同的ensemble方式：adaboost集成算法；默认权重值相等，都为1/2
    ```sh
    python Ensemble_Classifier.py
    python ensemble_classifier_with_equal_weight.py
    ```
注意：你需要在对BERT 模型进行微调，并将ML模型训练完成后再执行此操作：



Follow these steps to reproduce the tool and validate its effectiveness in detecting malicious PyPI packages.
