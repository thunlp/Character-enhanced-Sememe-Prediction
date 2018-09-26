#import cPickle as pickle;
import pickle
import sys;
import math;
import numpy as np;
import codecs
#import codecs
if (len(sys.argv)<4):
    print("Parameters insufficients");
hownet_filename = sys.argv[4];
model1_filename = sys.argv[1];
model2_filename = sys.argv[2];
ratio = float(sys.argv[3]);
output_filename = sys.argv[5];
model_filename = sys.argv[6];
with open(model1_filename,'rb') as model1_file:
    with open(model2_filename,'rb') as model2_file:
        model1 = [];
        model2 = [];
        print('Loading Models...')
        while True:
            try:
                model1.append(pickle.load(model1_file))
                model2.append(pickle.load(model2_file))
                model1[0]= dict(model1[0])
                model2[0]= dict(model2[0])
                print(len(model1[0].keys()),model1[0].keys())
                print(len(model2[0].keys()),model2[0].keys())
                model1_key = [x.encode("utf-8") for x in model1[0].keys()]
                model2_key = [x for x in model2[0].keys()]
                print(len(set(model1_key) & set(model2_key)))
                sys.exit()
            except EOFError: 
                break;
        print('Loading Models Complete, have read %d results from model1, %d results from model2' % (len(model1),len(model2)))
        assert(len(model1) == len(model2))
        index = 0;
        length = len(model1);
        test_words = [];
        print('Loading test files')
        with open(hownet_filename,'r') as test:
            for line in test:
                test_words.append(line.strip());
        print('Loading Complete,training beginning.')
        with codecs.open(output_filename,'w',encoding="utf8") as output:
            with open(model_filename,'wb') as model_file:
                while (index < length):
                    predict0 = dict(model1[index]);
                    predict1 = dict(model2[index]);
                    predict = [];
                    for key in predict0:
                        predict.append((key,ratio/(1+ratio)*(predict0[key])+1/(1+ratio)*predict1[key]));
                    predict.sort(key=lambda x:x[1],reverse=True);
                    result = [x[0] for x in predict];
                    target_str = test_words[index]+'\n'
                    #print([(type(x),x) for x in result])
                    #print(type(target_str),target_str)
                    result_str = ' '.join([x.decode('utf-8') for x in result])+"\n"
                    target_str = target_str.decode('utf-8')
                    target_str += result_str
                    #target_str = target_str.decode('utf-8')
                    output.write(target_str);
                    pickle.dump(predict,model_file)
                    index += 1;
        print('Training complete.')        
            
            
