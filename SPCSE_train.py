from __future__ import division
import numpy as np
import pickle
import random
import math
import sys
import codecs
from scipy import spatial

np.set_printoptions(threshold=np.nan)
reload(sys)
sys.setdefaultencoding("utf-8")
if (len(sys.argv) < 5):
    exit(0)
hownet_filename = sys.argv[1]
char_embedding_filename = sys.argv[2]
sememe_all_filename = sys.argv[3]
target_filename = sys.argv[4]
para_lambda = 0.1
max_iter = 20
num_cluster = 3
learning_rate = 0.01

word2id = {}
id2word = {}
char2id = {}
id2char = {}
sememe2id = {}
id2sememe = {}
wordid2charids = []
wordid2sememeids = {}
char_embedding_vec = {}

with codecs.open(hownet_filename, 'r') as hownet:
    with codecs.open(char_embedding_filename, 'r') as char_embedding_file:
        with codecs.open(sememe_all_filename, 'r') as sememe_all:
            # read sememe
            sememes_buf = sememe_all.readlines()
            sememes = sememes_buf[1].strip().strip('[]').split(' ')
            sememes = [sememe.strip().strip('\'') for sememe in sememes]
            sid = 0
            for s in sememes:
                sememe2id[s] = sid
                id2sememe[sid] = s
                sid += 1
            sememe_num = len(sememes)

            # read char emb
            line = char_embedding_file.readline()
            arr = line.strip().split()
            char_num = int(arr[0])
            dim_size = int(arr[1])
            W = np.zeros((char_num, num_cluster, dim_size), dtype=np.float64)
            cid = 0
            for line in char_embedding_file:
                try:
                    arr = line.strip().split()
                    float_arr = []
                    now_chr = arr[0].strip().decode('utf8')
                    now_pos = arr[1].strip()
                    if (now_pos not in ["b","m","e"]):
                        continue
                    com_chr = now_chr
                    if com_chr not in char2id:
                        char2id[com_chr] = cid
                        id2char[cid] = com_chr
                        cid += 1
                        if cid % 10000 == 0:
                            print 'cid: ' + str(cid)
                    now_cid = char2id[com_chr]
                    for i in range(2, 2 + dim_size):
                        float_arr.append(float(arr[i]))
                    regular = math.sqrt(sum([x * x for x in float_arr]))
                    if com_chr not in char_embedding_vec:
                        char_embedding_vec[com_chr] = []
                    char_embedding_vec[com_chr].append([])
                    cluster_id = len(char_embedding_vec[com_chr]) - 1
                    for i in range(2, 2 + dim_size):
                        char_embedding_vec[com_chr][-1].append(float(arr[i]) / regular)
                        W[now_cid][cluster_id][i-2] = float(arr[i]) / regular
                except Exception as e:
                    print line
                    raise e
            print('Embedding reading complete')

            # read hownet
            wid = 0
            while True:
                word = hownet.readline().strip()
                sememes_tmp = hownet.readline().strip().split()
                if (word or sememes_tmp):
                    wordid2sememeids[wid] = []
                    word2id[word] = wid
                    id2word[wid] = word
                    wordid2charids.append([])
                    w_utf8 = word.decode('utf8')
                    css = 0
                    l = len(w_utf8)
                    for c in w_utf8:
                        try:
                            if (c not in char2id):
                                continue
                            wordid2charids[wid].append(char2id[c])
                        except Exception as e:
                            print(word, c)
                            raise e
                            sys.exit()
                        css += 1
                    length = len(sememes_tmp)
                    for i in range(0, length):
                        wordid2sememeids[wid].append(sememe2id[sememes_tmp[i]])
                    wid += 1
                    if wid % 1000 == 0:
                        print 'wid: ' + str(wid)
                else:
                    break
            print("hownet reading complete")
            word_num = len(word2id)

            # Read PMI
            with open('PMI.txt', 'r') as PMI:
                P = []
                for line in PMI:
                    arr = line.strip().split()
                    arr = [float(e) for e in arr]
                    P.extend(arr)
                P = np.array(P).reshape(sememe_num, sememe_num)
                M = np.zeros((word_num, sememe_num))
                for wid in range(0, word_num):
                    try:
                        for sid in wordid2sememeids[wid]:
                            M[wid][sid] = 1
                    except:
                        print(word)
                        sys.exit()
            print("PMI calculating complete")


            sememe_embedding = (np.random.randn(sememe_num * 2, dim_size) - 0.5) / dim_size
            bias_sememe = (np.random.randn(sememe_num, 1) - 0.5) / dim_size
            bias_char = (np.random.randn(char_num, 1) - 0.5) / dim_size
            try:
                print('Try to read from checkpoint')
                target = open(target_filename, 'rb')
                sememe_embedding = pickle.load(target)
                bias_char = pickle.load(target)
                bias_sememe = pickle.load(target)
                print('checkpoint reading complete')
                target.close()
            except:
                print('checkpoint reading failed, initialize with random value')

            with open(target_filename, 'wb') as target:
                sememe_embedding_dersum = np.ones((sememe_num * 2, dim_size))
                bias_sememe_dersum = np.ones((sememe_num, 1))
                bias_char_dersum = np.ones((char_num, 1))
                print('Initailization complete')
                for i in range(1, max_iter):
                    print("Process:%f" % (i / max_iter))
                    loss = 0
                    count = 0
                    for j in range(word_num):
                        for i in range(0, sememe_num):
                            sem0 = sememe_embedding[2 * i]
                            sem1 = sememe_embedding[2 * i + 1]
                            der = np.zeros((1, dim_size))
                            if (M[j][i] == 0):
                                rand = random.randint(1, 1000)
                                if (rand > 25):
                                    continue
                            count += 1
                            best_v = 100
                            best_i = -1
                            best_k = -1
                            for cid in wordid2charids[j]:
                                for kk in range(num_cluster):
                                    v = spatial.distance.cosine(W[cid][kk].reshape(1, dim_size), (sem0 + sem1)) #distance
                                    if v < best_v:
                                        best_v = v
                                        best_i = cid
                                        best_k = kk
                            w = W[best_i][best_k].reshape(1, dim_size)
                            delta = W[best_i][best_k].reshape(1, dim_size).dot((sem0 + sem1).transpose()) + bias_sememe[i] + bias_char[best_i] - M[j][i]
                            loss += delta ** 2
                            der += delta * 2 * w
                            der = der.reshape(dim_size, )
                            sememe_embedding[2 * i] += -learning_rate * der / sememe_embedding_dersum[2 * i]
                            sememe_embedding[2 * i + 1] += -learning_rate * der / sememe_embedding_dersum[2 * i + 1]
                            sememe_embedding_dersum[2 * i] += der ** 2
                            sememe_embedding_dersum[2 * i + 1] += der ** 2
                            bias_char[best_i] += 2 * delta * learning_rate / bias_char_dersum[best_i]
                            bias_char_dersum[best_i] += 4 * delta ** 2
                            bias_sememe[i] += 2 * delta * learning_rate / bias_sememe_dersum[i]
                            bias_sememe_dersum[i] += 4 * delta ** 2
                    for j in range(0, sememe_num):
                        for i in range(0, sememe_num):
                            sem0 = sememe_embedding[2 * j]
                            sem1 = sememe_embedding[2 * i + 1]
                            der = np.zeros((1, dim_size))
                            der_out = np.zeros((1, dim_size))
                            if (P[j][i] == 0):
                                rand = random.randint(1, 1000)
                                if (rand > 5):
                                    continue
                            count += 1
                            delta = sem0.dot((sem1).transpose()) - P[j][i]
                            loss += para_lambda * delta ** 2

                            der += para_lambda * delta * 2 * sem0
                            der = der.reshape(dim_size, )
                            sememe_embedding[2 * i + 1] += -learning_rate * der / sememe_embedding_dersum[2 * i + 1]
                            sememe_embedding_dersum[2 * i + 1] += der ** 2

                            der_out += para_lambda * delta * 2 * sem1
                            der_out = der_out.reshape(dim_size, )
                            sememe_embedding[2 * j] += -learning_rate * der_out / sememe_embedding_dersum[2 * j]
                            sememe_embedding_dersum[2 * j] += der_out ** 2

                    print("loss:%f" % (loss / count,))
                pickle.dump(sememe_embedding, target)
                pickle.dump(bias_char, target)
                pickle.dump(bias_sememe, target)

