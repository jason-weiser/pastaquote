import random
import json
import os
import pickle
from run_list import RunList

def r_run(parent_dir):
    with open(os.path.join(parent_dir, 'data/quotes.json'),"r") as json_file:
        data = json.load(json_file)
        n = random.randint(0,len(data)-1)
        tweet = "{}".format(data[n]['quote'])
        working_data = data[:]
        working_data.pop(n)

    if len(working_data) == 0:
        runlist = RunList(parent_dir)
        runlist.runit()
    else:
        with open(os.path.join(parent_dir,'data/quotes.json'), "w") as f:
            json.dump(working_data, f, indent=4)
    return tweet

def s_run(parent_dir):
    with open(os.path.join(parent_dir, 'data/quotes.json')) as json_file:
        data = json.load(json_file)
        n = pickle.load(open(os.path.join(parent_dir,'data/number.p'),"rb"))
        tweet = "{}".format(data[n]['quote'])
        if n == len(data)-1:
            n = 0
        else:
            n += 1
        pickle.dump(n, open(os.path.join(parent_dir,'data/number.p'), "wb"))
    return tweet

if __name__ == "__main__":
    pass
