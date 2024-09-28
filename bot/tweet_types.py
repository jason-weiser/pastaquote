import random
import json
import os
import pickle
from run_list import RunList
from useful_resources import pull_config

def add_hashtags(base_post, where_posting):
    platform = pull_config(where_posting)
    if platform['ENABLE_HASHTAGS']:
        base_post += "\n\n"
        for i in platform['HASHTAGS']:
            base_post += "#{} ".format(i)
        return base_post
    else:
        return base_post

def r_run(parent_dir, list_loc):
    with open(os.path.join(parent_dir, 'data/quotes.json'),"r") as json_file:
        data = json.load(json_file)
        n = random.randint(0,len(data)-1)
        tweet = "{}".format(data[n])
        working_data = data[:]
        working_data.pop(n)

    if len(working_data) == 0:
        runlist = RunList(parent_dir,list_loc)
        runlist.runit()
    else:
        with open(os.path.join(parent_dir,'data/quotes.json'), "w") as f:
            json.dump(working_data, f, indent=4)
    return tweet

def s_run(parent_dir):
    with open(os.path.join(parent_dir, 'data/quotes.json')) as json_file:
        data = json.load(json_file)
        n = pickle.load(open(os.path.join(parent_dir,'data/number.p'),"rb"))
        tweet = "{}".format(data[n])
        if n == len(data)-1:
            n = 0
        else:
            n += 1
        pickle.dump(n, open(os.path.join(parent_dir,'data/number.p'), "wb"))
    return tweet

if __name__ == "__main__":
    pass
