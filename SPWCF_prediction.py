# -*- coding: utf-8 -*-
import sys
import cPickle as pickle

hownet_filename = sys.argv[1]
sememe_all_filename = sys.argv[2]
test_filename = sys.argv[3]
output_filename = sys.argv[4]
model_filename = sys.argv[5]

with open(hownet_filename,'r') as hownet:
    with open(sememe_all_filename,'r') as sememe_all:
        with open(test_filename, 'r') as test_file:
            with open(output_filename, 'wb') as output_file:
                with open(model_filename,'wb') as model_file:
                    sememes_buf = sememe_all.readlines()
                    sememes = sememes_buf[1].strip().strip('[]').split(' ')
                    sememes = [sememe.strip().strip('\'') for sememe in sememes]
                    sememe_size = len(sememes)
                    hownet_words = []
                    characters = []
                    #read sememe complete
                    word2sememe = {}
                    char2sememe = {}
                    sememe2char = {}
                    while True:
                        word = hownet.readline().strip()
                        sememes_tmp = hownet.readline().strip().split()
                        if (word or sememes_tmp):
                            word2sememe[word] = []
                            hownet_words.append(word)
                            length = len(sememes_tmp)
                            for i in range(0,length):
                                word2sememe[word].append(sememes_tmp[i])
                        else: break; 
                    #read hownet complete
                    print("hownet reading complete")

                    for w in word2sememe:
                        w_utf8 = w.decode('utf8')
                        l = len(w_utf8)
                        ss = 0
                        for c in w_utf8:
                            if ss == 0:
                                c = c + '_h'
                                if c not in characters:
                                    characters.append(c)
                            if ss == l-1:
                                c = c + '_t'
                                if c not in characters:
                                    characters.append(c)
                            if (ss > 0 and ss < l-1) or (l == 1):
                                c = c + '_m'
                                if c not in characters:
                                    characters.append(c)
                            ss += 1
                    
                    for c in characters:
                        char2sememe[c] = {}
                        for s in sememes:
                            char2sememe[c][s] = 0
                    
                    for s in sememes:
                        sememe2char[s] = {}
                        for c in characters:
                            sememe2char[s][c] = 0

                    for w in word2sememe:
                        w_utf8 = w.decode('utf8')
                        l = len(w_utf8)
                        ss = 0
                        for c in w_utf8:
                            
                            if ss == 0:
                                c = c + '_h'
                                for sememe in word2sememe[w]:
                                    sememe2char[sememe][c] += 1
                                    char2sememe[c][sememe] += 1
                            if ss == l-1:
                                c = c + '_t'
                                for sememe in word2sememe[w]:
                                    sememe2char[sememe][c] += 1
                                    char2sememe[c][sememe] += 1
                            if (ss > 0 and ss < l-1) or (l == 1):
                                c = c + '_m'
                                for sememe in word2sememe[w]:
                                    sememe2char[sememe][c] += 1
                                    char2sememe[c][sememe] += 1
                            ss += 1

                    num = 0
                    for c in char2sememe:
                        for s in char2sememe[c]:
                            num  += char2sememe[c][s]                        
                    print 'Ave. sememe per char :' + str(float(num) / len(char2sememe))

                    num = 0
                    for s in sememe2char:
                        for c in sememe2char[s]:
                            num += sememe2char[s][c]
                    print 'Ave. char per sememe :' + str(float(num) / len(sememe2char))


                    for c in char2sememe:
                        sum = 0
                        for s in char2sememe[c]:
                            sum += char2sememe[c][s]
                        if sum != 0:
                            for s in char2sememe[c]:
                                char2sememe[c][s] /= float(sum)

                    for s in sememe2char:
                        sum = 0
                        for c in sememe2char[s]:
                            sum += sememe2char[s][c]
                        if sum != 0:
                            for c in sememe2char[s]:
                                sememe2char[s][c] /= float(sum)

                    test_data = test_file.readlines()
                    test_data = [t.strip() for t in test_data]
                    test_list = []
                    for w in test_data:
                        w_utf8 = w.decode('utf8')
                        sememes_rank = {}
                        for sememe in sememes:
                            sememes_rank[sememe] = 0
                        css = 0
                        l = len(w_utf8)
                        for c in w_utf8:
                            if css == 0:
                                c = c + '_h'
                                if c in char2sememe:
                                    for s in char2sememe[c]:
                                        sememes_rank[s] += char2sememe[c][s]
                            if css == l-1:
                                c = c + '_t'
                                if c in char2sememe:
                                    for s in char2sememe[c]:
                                        sememes_rank[s] += char2sememe[c][s]
                            if (css > 0 and css < l-1) or (l == 1):
                                c = c + '_m'
                                if c in char2sememe:
                                    for s in char2sememe[c]:
                                        sememes_rank[s] += char2sememe[c][s]
                            css += 1
                        reslist = []
                        for s in sememes_rank:
                            reslist.append((s, sememes_rank[s]))
                        reslist.sort(key=lambda x:x[1],reverse=True)
                        final = []
                        for sememe,score in reslist:
                            final.append(sememe)
                        print("Process:%f" %(float(len(test_list)) / len(test_data)))
                        test_list.append(w)
                        output_file.write(w.strip()+"\n")
                        output_file.write(' '.join(final)+"\n")
                        pickle.dump(reslist,model_file)

