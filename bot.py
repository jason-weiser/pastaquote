import json
import pickle
import os
import sys
import argparse
from twitter import Twitter
from run_list import RunList
import logging

## Arguments for command-line use
parser = argparse.ArgumentParser(
    description='A command line python bot to tweet from a csv list'
   )
parser.add_argument('--process', help="run when added new items", \
                    dest="process_list", action="store_true")
parser.add_argument('--init', help='converts csv, starts numbering', \
                    dest='initialize', action="store_true")
parser.add_argument("--tweet", help="tweets the next item in the list", \
                    dest='tweet', action='store_true')
args=parser.parse_args()

## Logging

logging_file = os.path.join(os.getenv('HOME'),'twitterbot.log')

logging.basicConfig(
    level=logging.INFO,
    format ='%(asctime)s : %(levelname)s : %(message)s',
    filename=logging_file,
    filemode='a+',
)

## Program run

def make_pickle():
    initial_num = 0
    pickle.dump(initial_num, open("number.p","wb"))

def tweet_it():
    with open('files/quotes.json') as json_file:
        n = pickle.load(open("number.p","rb"))
        data = json.load(json_file)
        tweet = "{}\n\t---{}".format(data[n]['quote'],data[n]['author'])
        print(tweet)
        logging.info("Tweeted \'" + tweet + "\'")
#        print(f"{data[n]['quote']}\n\t---{data[n]['author']}")
        if n == len(data)-1:
            n = 0
        else:
            n += 1
        logging.info("Tweet sent succesfully! Next number is {}".format(n))
        pickle.dump(n, open("number.p","wb"))

def main():
    runlist = RunList()
    twitter = Twitter()
    if not os.path.isfile("number.p"):
        make_pickle()
        logging.info("Pickle made and set to zero")
    if args.process_list:
        runlist.runit()
        logging.info("CSV list successfully converted to json")
    if args.initialize:
        runlist.runit()
        make_pickle()
        msg = "Numbering started and list converted. Ready to tweet!"
        print(msg)
        logging.info("CSV converted and pickle created. Initialization successful")
    if args.tweet:
        tweet_it()
    elif not(args.tweet or args.process_list or args.initialize):
        print("One argument is required. See --help for details")

if __name__ == "__main__":
    main()
