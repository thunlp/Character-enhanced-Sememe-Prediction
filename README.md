# Character-enhanced-Sememe-Prediction

## Table of contents

* [Introduction](#introduction)
* [Usage](#usage)
   * [Preparation ](#preparation)
   * [Training and Prediction](#training-and-prediction)
* [References](#references)


## Introduction
The code for **Incorporating Chinese Characters of Words for Lexical Sememe Prediction (ACL2018) [1]**

## Usage
### Preparation 
1. Prepare a file that contains pre-trained Chinese word embeddings(of Google Word2Vec form). We recommend that the amount of words be at least 200,000 and the number of dimentions be at least 200. It will achieve much better result using a large (20GB or more is recommended) corpus to train your embeddings for running this program. 

2. Rename the word embedding file as `embedding_200.txt` and put it in the repository root directory.

3. Prepare a file that contains pre-trained Chinese character embeddings(of CWE form; see paper [2] and [code](https://github.com/Leonard-Xu/CWE)). We recommend that the number of dimentions be at least 200. It will achieve much better result using a large (20GB or more is recommended) corpus to train your embeddings for running this program.

4. Rename the word embedding file as `char_embedding_200.txt` and put it in the repository root directory.

5. Run `data_generator.sh`, the program will automatically generate evaluation data set and other data files required during training.

### Training and Prediction
1. Run `SPWCF.sh`/`SPCSE.sh` The corresponding model will be automatically learned and evaluated.

2. Since we need SPWE and SPSE as a part of our model, see paper [3] and [code](https://github.com/thunlp/sememe_prediction) for details. Please use SPWE and SPSE to get the model files `model_SPWE` and `model_SPSE` and copy them to the root directory of this repository.

3. Run `CSP.sh` The corresponding model will be automatically learned and evaluated.


## References
[1] Huiming Jin, Hao Zhu, Zhiyuan Liu, Ruobing Xie, Maosong Sun, Fen Lin, and Leyu Lin. 2018. Incorporating Chinese Characters of Words for Lexical Sememe Prediction. In Proceedings of ACL.

[2] Xinxiong Chen, Lei Xu, Zhiyuan Liu, Maosong Sun, and Huan-Bo Luan. 2015. Joint Learning of Character and Word Embeddings. In Proceedings of IJCAI.

[3] Ruobing Xie, Xingchi Yuan, Zhiyuan Liu, and Maosong Sun. 2017. Lexical sememe prediction via word embeddings and matrix factorization. In Proceedings of IJCAI
