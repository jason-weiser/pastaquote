import random
import json
import os
from run_list import RunList

with open('/home/jason/python/twitterbot/data/quotes.json',"r") as json_file:
    n = 0
    data = json.load(json_file)
    n = random.randint(0,len(data)-1)
    print(f"n equals {n}")
    tweet = "{}\n\t---{}".format(data[n]['quote'],data[n]['author'])
    print(tweet)
#    data[n]["used"] = 1
print(f"length of data is {len(data)}")
working_data = data[:]
print(f"length of working_data is {len(working_data)}")
print(f"n equals{n}")
working_data.pop(n)
print(f"new length of working_Data is {len(working_data)}")

if len(working_data) == 0:
    runlist = RunList("/home/jason/python/twitterbot/")
    runlist.runit()
else:
    os.remove('/home/jason/python/twitterbot/data/quotes.json')
    with open('/home/jason/python/twitterbot/data/quotes.json',"w") as f:
        json.dump(working_data, f)
#f.close()
