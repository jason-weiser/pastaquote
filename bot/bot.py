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
from useful_resources import connection_validator
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
parser.add_argument("--post", help="posts the next item in the list", \
                    dest='post', action='store_true')
args=parser.parse_args()


## Find parent directory
running_file = Path(__file__)
current_dir = running_file.resolve().parents[0]
parent_dir = running_file.resolve().parents[1]
pickle_dir = os.path.join(parent_dir, "data/number.p")

## Load the config
options = pull_config('SETUP')
twitter_options = pull_config('TWITTER')
mastodon_options = pull_config('MASTODON')

##Define objects

runlist = RunList(parent_dir, options['CSV_LOCATION'])
twitter = Twitter()
masto = Masto()

## Program run

##This is for the sequential posting, only.
#https://docs.python.org/3/library/pickle.html
def make_pickle():
    initial_num = 0
    pickle.dump(initial_num, open(pickle_dir,"wb"))

def actually_post(tweet):
        if twitter_options['ENABLE_PLATFORM'] == True:
            log_this("Tweet attempted: {}\nResponse: {}" \
                    .format(tweet_types.add_hashtags(tweet, 'TWITTER'), \
                        twitter.post_tweet(\
                            tweet_types.add_hashtags(tweet, 'TWITTER'))))
        else:
            log_this("Twitter not enabled in config. Skipping.")
        if mastodon_options['ENABLE_PLATFORM'] == True:
            log_this("Toot attempted: {}\nResponse: {}" \
                    .format(tweet_types.add_hashtags(tweet, 'MASTODON'), \
                        masto.tootit(\
                            tweet_types.add_hashtags(tweet, 'MASTODON'))))
        else:
            log_this("Mastodon not enabled in config. Skipping.")

def tweet_it():
    if options['TYPE'] == "sequential":
        post_content = tweet_types.s_run(parent_dir)
        actually_post(post_content)
    elif options['TYPE'] == "random":
        post_content = tweet_types.r_run(parent_dir)
        actually_post(post_content)

def lets_post():
    where_csv = pull_config('SETUP')['CSV_LOCATION']
    if not os.path.isdir(os.path.join(parent_dir, "data/")):
        os.mkdir(os.path.join(parent_dir, "data/"))
    else:
        pass
    if not (options['TYPE'] == "sequential" or options['TYPE'] == "random"):
        print("""
        You need to choose the order in which the list will run
        Please edit the config file in config.yaml
        """)
        sys.exit()
    else:
        pass
    if not os.path.isdir(where_csv) and \
        not connection_validator(where_csv) == 200:
        error_msg = """There's an issue with your CSV file. Either the server couldn't connect
to the webpage or the file doesn't exist. Please fix this and run again."""
        print(error_msg)
        log_this(error_msg)
        sys.exit()
    else:
        pass
    #if there isn't a numbering file in place and you want sequential tweets
    #this makes a number file
    if not os.path.isfile(pickle_dir):
        make_pickle()
        log_this("Numbering started and set to zero")
    else:
        pass
    #converts new csv list to json
    #reset all settings
    if args.initialize:
        runlist.runit()
        make_pickle()
        msg = "Numbering started and list converted. Ready to tweet!"
        print(msg)
        log_this("CSV converted and pickle created. Initialization successful")
    #authenticates and tweets
    if args.post:
        tweet_it()
    elif not(args.post or args.initialize):
        print("One argument is required. See --help for details")
        log_this("Script run without argument. Nothing posted.")

def main():
    try:  
        lets_post()
    except Exception as e: 
        print(e)
        log_this(e)

if __name__ == "__main__":
    main()