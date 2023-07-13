import random
import json
import pickle
import os
import sys
import argparse
import yaml
import tweet_types
from useful_resources import log_this
from useful_resources import pull_config
from pathlib import Path
from platforms import Twitter
from platforms import Masto
from run_list import RunList

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


## Find parent directory
running_file = Path(__file__)
current_dir = running_file.resolve().parents[0]
parent_dir = running_file.resolve().parents[1]
pickle_dir = os.path.join(parent_dir, "data/number.p")

## Load the config
#with open(os.path.join(current_dir,'config.yaml')) as config_yml:
#    config = yaml.safe_load(config_yml)
options = pull_config('SETUP')
twitter_options = pull_config('TWITTER')
mastodon_options = pull_config('MASTODON')

##Define objects

runlist = RunList(parent_dir, options['CSV_LOCATION'])
twitter = Twitter()
masto = Masto()

## Program run

def make_pickle():
    initial_num = 0
    pickle.dump(initial_num, open(pickle_dir,"wb"))

def actually_post(tweet):
        if twitter_options['ENABLE_TWITTER'] == True:
            log_this("Tweet attempted: {}.\nResponse: {}" \
                    .format(tweet.rstrip('\n'), \
                        twitter.post_tweet(tweet_types.add_hashtags(tweet, 'TWITTER'))))

        else:
            log_this("Twitter not enabled in config. Skipping.")
        if mastodon_options['ENABLE_MASTODON'] == True:
            log_this("Post attempted: {}.\nResponse: {}" \
                    .format(tweet.rstrip('\n'), \
                        masto.tootit(tweet_types.add_hashtags(tweet, 'MASTODON'))))
        else:
            log_this("Mastodon not enabled in config. Skipping.")

def tweet_it():
    if options['TYPE'] == "sequential":
        post_content = tweet_types.s_run(parent_dir)
        actually_post(post_content)
    elif options['TYPE'] == "random":
        post_content = tweet_types.r_run(parent_dir)
        actually_post(post_content)

def main():
    #ensure that there is a mode file or create one with argparse
    #also makes new json because you will have an incomplete file
    #when switching from random to sequential
    if not (options['TYPE'] == "sequential" or options['TYPE'] == "random"):
        print("""
        You need to choose the order in which the list will run
        Please edit the config file in config.yaml
        """)
    #if there isn't a numbering file in place and you want sequential tweets
    #this makes a number file
    if not os.path.isfile(pickle_dir):
        make_pickle()
        log_this("Numbering started and set to zero")
    #converts new csv list to json
    #reset all settings
    if args.initialize:
        runlist.runit()
        make_pickle()
        msg = "Numbering started and list converted. Ready to tweet!"
        print(msg)
        log_this("CSV converted and pickle created. Initialization successful")
    #authenticates and tweets
    if args.tweet:
        tweet_it()
    elif not(args.tweet or args.initialize):
        print("One argument is required. See --help for details")
        log_this("Script run without argument. Nothing happened")

if __name__ == "__main__":
    main()

##TODO: add CSV location to only run_list.py
##TODO: check for whitespace in list of hashtags, remove it, capitalize second word, combine