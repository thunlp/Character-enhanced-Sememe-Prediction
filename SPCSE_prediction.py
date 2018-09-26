# -*- coding: utf-8 -*-
import numpy as np
import pickle
import random
import math
import sys
import codecs
from scipy import spatial

sys.setdefaultencoding = "utf-8"
char_embedding_filename = sys.argv[1]
sememe_all_filename = sys.argv[2]
spce_embedding_filename = sys.argv[3]
question_filename = sys.argv[4]
target_filename = sys.argv[5]
model_filename = sys.argv[6]
num_cluster = 3
char2id = {}
id2char = {}
sememe2id = {}
id2sememe = {}
char_embedding_vec = {}

with codecs.open(char_embedding_filename, 'r') as char_embedding_file:
    with codecs.open(sememe_all_filename, 'r') as sememe_all:
        with codecs.open(spce_embedding_filename, 'rb') as spce_embedding_file:
            with codecs.open(question_filename, 'r') as question_file:
                with codecs.open(target_filename, 'w') as output:
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

                    line = char_embedding_file.readline()
                    arr = line.strip().split()
                    char_num = int(arr[0])
                    dim_size = int(arr[1])
                    W = np.zeros((char_num, num_cluster, dim_size), dtype=np.float64)
                    cid = 0
                    for line in char_embedding_file:
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
                    print('Embedding reading complete')

                    sememe_embedding = pickle.load(spce_embedding_file)
                    bias_char = pickle.load(spce_embedding_file)
                    bias_sememe = pickle.load(spce_embedding_file)

                    ss = 0
                    for line in question_file:
                        output.write(line.strip()+'\n')
                        word = line.strip()
                        w_utf8 = word.decode('utf8')
                        scores = []
                        for i in range(sememe_num):
                            sem0 = sememe_embedding[2 * i]
                            sem1 = sememe_embedding[2 * i + 1]
                            best_v = 100
                            best_c = -1
                            best_k = -1
                            for ch in w_utf8:
                                cid = char2id[ch]
                                for kk in range(num_cluster):
                                    w = W[cid][kk].reshape(1, dim_size)
                                    v = spatial.distance.cosine(W[cid][kk].reshape(1, dim_size), (sem0 + sem1)) #distance
                                    if v < best_v:
                                        best_v = v
                                        best_c = cid
                                        best_k = kk
                            scores.append((id2sememe[i], 1-best_v))
                        scores.sort(key=lambda x:x[1],reverse=True)
                        result = [x[0] for x in scores]
                        output.write(" ".join((result))+'\n')
                        with open(model_filename,'ab') as model_file:
                            pickle.dump(scores,model_file)
                        ss += 1
                        if ss % 100 == 0:
                            print ss




                    '''
                    for ch in test_chars:
                        cid = char2id[ch]
                        print ch + ' cid: ' + str(cid)
                        scores = []
                        for i in range(sememe_num):
                            sem0 = sememe_embedding[2 * i]
                            sem1 = sememe_embedding[2 * i + 1]
                            best_v = 100
                            best_k = -1
                            for kk in range(num_cluster):
                                w = W[cid][kk].reshape(1, dim_size)
                                v = abs(W[cid][kk].reshape(1, dim_size).dot((sem0 + sem1).transpose()) + bias_sememe[i] + bias_char[cid] - 1)
                                print id2sememe[i], kk, v, np.sqrt(np.sum(W[cid][kk] * W[cid][kk]))
                                if v < best_v:
                                    best_v = v
                                    best_k = kk
                            scores.append((i, best_v, best_k))
                        scores.sort(key=lambda x:x[1],reverse=False)
                        output_f.write(ch.encode('utf-8'))
                        for s in scores:
                            output_f.write('(' + str(id2sememe[s[0]]) + ', ' + str(s[1]) + ', ' + str(s[2]) + ')  ')
                        output_f.write('\n')

                    print np.sqrt(np.sum(W[:,0,:] * W[:,0,:]))/W.shape[0], np.sqrt(np.sum(W[:,1,:] * W[:,1,:]))/W.shape[0], np.sqrt(np.sum(W[:,2,:] * W[:,2,:]))/W.shape[0]
                    '''

                                

