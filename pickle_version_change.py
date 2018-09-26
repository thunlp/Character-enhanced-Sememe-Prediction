# contributed by Chenghao Yang
# because the implementation of SPWE && SPSE has been upgraded to python3, users of CSP may need this code to change the version of pickle protocol of python3 to python2

import pickle

file_list = ["model_SPWE_jhm","model_SPSE_jhm"]
out_list = ["model_SPWE","model_SPSE"]
#file_list = ["model_SPSE_jhm"]
#out_list = ["model_SPSE"]

for filename,outname in zip(file_list,out_list):
    #with open(filename,"rb") as f:
    tmp = list()
    f = open(filename,"rb")
    while True:
        try:
            tmp.append(pickle.load(f))
        except EOFError:
            f.close()
            break
    f_out = open(outname,"wb")
    if (len(tmp)==1):
        tmp = tmp[0]
    for item in tmp:
        res = dict()
        #print(len(item))
        for (key,val) in item:
            res[key] = val
        pickle.dump(res,f_out,protocol=2)
