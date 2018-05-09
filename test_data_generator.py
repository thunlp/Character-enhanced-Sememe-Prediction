# -*- coding: utf-8 -*-
# Generate test and validation set
import sys
import random
reload(sys)
sys.setdefaultencoding="utf-8"
if (len(sys.argv)<3):
    print 'no enough parameter'
    exit()
hownet_filename = sys.argv[1]
embedding_filename = sys.argv[2]
test_answer_filename = hownet_filename+"_test_answer"
test_input_filename = hownet_filename+"_test_input"
var_answer_filename = hownet_filename+"_var_answer"
var_input_filename = hownet_filename+"_var_input"
with open(hownet_filename,'r') as hownet:
    with open(test_input_filename,'w') as test_input:
        with open(test_answer_filename,'w') as test_answer:
            with open(var_input_filename,'w') as var_input:
                with open(var_answer_filename,'w') as var_answer:
                    with open(embedding_filename,'r') as embedding:
                        data = hownet.readlines()
                        dataBuf = []
                        for line in data:
                            dataBuf.append(line.strip())
                        data = dataBuf
                        wordsBuf = embedding.readlines()
                        sourcewords = []
                        length = len(wordsBuf)
                        for i in range(1,length):
                            line = wordsBuf[i].strip()
                            arr = line.split()
                            sourcewords.append(arr[0])
                        words = data[0::2]
                        sememes = data[1::2]
                        data = list(zip(words,sememes))
                        samples_test_var = random.sample(sourcewords,int(len(sourcewords)*0.2))
                        samples_test = random.sample(samples_test_var,int(len(samples_test_var)*0.5))
                        
                        
                        samplesBuf = []
                        # output test data
                        for word in samples_test:
                            try:
                                position = words.index(word.strip())
                                sememe = sememes[position]
                                samplesBuf.append((word,sememe))
                            except:
                                print samples_test.index(word)
                        for word,sememe in samplesBuf:
                            test_input.write(word+'\n')
                            test_answer.write(word+'\n'+sememe+'\n')

                        samplesBuf_var = []
                        # output var data
                        for word in samples_test_var:
                            if word not in samples_test:
                                try:
                                    position = words.index(word.strip())
                                    sememe = sememes[position]
                                    samplesBuf.append((word,sememe))
                                    samplesBuf_var.append((word,sememe))
                                except:
                                    print samples_test_var.index(word)
                        for word,sememe in samplesBuf_var:
                            var_input.write(word+'\n')
                            var_answer.write(word+'\n'+sememe+'\n')

                        samples = samplesBuf
                        # output train data
                        with open('train_hownet','w') as train:
                            for word,sememe in zip(words,sememes):
                                try:
                                    position = samples.index((word,sememe))
                                except:
                                    train.write(word+'\n'+sememe+'\n')
                        
