#from __future__ import unicode_literals
import random
import json
import pickle
import os
import sys
import argparse
import tweet_types
from pathlib import Path
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

logging_file = os.path.join(os.environ['HOME'],'twitterbot.log')

logging.basicConfig(
    level=logging.INFO,
    format ='%(asctime)s : %(levelname)s : %(message)s',
    filename=logging_file,
    filemode='a+',
)

## Find parent directory
current_dir = Path(__file__)
parent_dir = current_dir.resolve().parents[1]
pickle_dir = os.path.join(parent_dir, "data/number.p")
mode_file = os.path.join(parent_dir, "data/mode.p")

##Define objects

runlist = RunList(parent_dir)
twitter = Twitter()

## Program run

def make_pickle():
    initial_num = 0
    pickle.dump(initial_num, open(pickle_dir,"wb"))

def tweet_it():
    w_mode = pickle.load(open(mode_file,"rb"))
    if w_mode == 2:
        tweet = tweet_types.s_run(parent_dir)
        logging.info("Tweet attempted: {}.\nResponse: {}" \
                    .format(tweet.rstrip('\n'), twitter.post_tweet(tweet)))
    elif w_mode == 1:
        tweet = tweet_types.r_run(parent_dir)
        logging.info("Tweet attempted: {}.\nResponse: {}" \
                    .format(tweet.rstrip('\n'), twitter.post_tweet(tweet)))
def main():
#    runlist = RunList(parent_dir)
#    twitter = Twitter()
    #ensure that there is a mode file or create one with argparse
    #also makes new json because you will have an incomplete file
    #when switching from random to sequential
    ## REMOVED
    #if there isn't a numbering file in place and you want sequential tweets
    #this makes a number file
    if not os.path.isfile(pickle_dir):
        make_pickle()
        logging.info("Pickle made and set to zero")
    #converts new csv list to json
    if args.process_list:
        runlist.runit()
        logging.info("CSV list successfully converted to json")
    #reset all settings
    if args.initialize:
        runlist.runit()
        make_pickle()
        msg = "Numbering started and list converted. Ready to tweet!"
        print(msg)
        logging.info("CSV converted and pickle created. Initialization successful")
    #authenticates and tweets
    if args.tweet:
        tweet_it()
    elif not(args.tweet or args.process_list or args.initialize):
        print("One argument is required. See --help for details")

if __name__ == "__main__":
    main()
