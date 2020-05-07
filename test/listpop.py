import random
import json

with open('/home/jason/python/twitterbot/data/quotes.json',"r+") as json_file:
    n = 0
    data = json.load(json_file)
    temp_data = data
    n = random.randint(0,len(temp_data)-1)
    print(f"n equals {n}")
    tweet = "{}\n\t---{}".format(data[n]['quote'],data[n]['author'])
    print(tweet)
    temp_data.pop(n)
    print(len(temp_data))
#    logging.info("Tweeted \'" + tweet + "\'")
#            data = json.load(json_file)
#        print(f"There are now {len(data)} items left in data")
#if len(data) == 0:
 #               runlist.runit()

