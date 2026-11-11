import random
import traceback
import json
import pickle
import os
import sys
import argparse
import yaml
import tweet_types
import logging
from useful_resources import log_this, pull_config, connection_validator, parent_dir, pickle_dir, create_file_in_data, print_and_log, setup_loggin
from pathlib import Path
from platforms import Masto, Bluesky, Twitter, Threads, platforms
from run_list import RunList

## Arguments for command-line use
parser = argparse.ArgumentParser(
    description='A command line python bot to tweet from a text list'
   )
parser.add_argument('--process', help="run when added new items", \
                    dest="process_list", action="store_true")
parser.add_argument('--init', help='converts text list, starts numbering', \
                    dest='initialize', action="store_true")
parser.add_argument("--post", help="posts the next item in the list", \
                    dest='post', action='store_true')
parser.add_argument("--add", help="adds items to running list", \
                    dest='add', action='store_true')
parser.add_argument("-y", help="approve auto-adding", \
                    dest='yes', action='store_true')
args=parser.parse_args()

## Create data folder if it doesn't exist
if not os.path.isdir(os.path.join(parent_dir, "data/")):
    os.mkdir(os.path.join(parent_dir, "data/"))

## Load the main options from config
options = pull_config('SETUP')

##Define list and posting destinations
runlist = RunList(parent_dir, options['LIST_LOCATION'])
destinations = list(platforms)

## Define the log
setup_logging(parent_dir)
log = logging.getLogger(__name__) 

## Program run

##This is for the sequential posting only.
#https://docs.python.org/3/library/pickle.html
def make_pickle():
    initial_num = 0
    pickle.dump(initial_num, open(pickle_dir,"wb"))

## Despite three functions having the word 'post' in them, this is what *actually* posts. It's the last in the line
## and it's what interfaces with the various APIs
def actually_post(tweet,platform_to_post):
    platform_dict = {
        'TWITTER': Twitter,
        'MASTODON': Masto,
        'BLUESKY': Bluesky,
        'THREADS': Threads
    }
    platform_function = platform_dict[platform_to_post]()
    if platform_function is None:
        msg = f"Platform ({platform_function}) not defined. Please add at least one platform to the config."
        print(msg)
        log.info(msg)

    platform_options = pull_config('PLATFORMS')[platform_to_post]
    if platform_options['ENABLE_PLATFORM'] == True and \
        not platform_options['SKIP_TOO_LONG'] and \
        runlist.validate_char(platform_to_post,tweet) == 0:
        log.info("Attempting post: {}\nResponse: {}" \
            .format(tweet_types.add_hashtags(tweet,\
            platform_to_post), \
            platform_function.post_it(\
            tweet_types.add_hashtags(tweet, platform_to_post))))
    elif platform_options['ENABLE_PLATFORM'] == False:
            log.info("{} not enabled in config. Skipping.".format(platform_to_post))
    elif platform_options['SKIP_TOO_LONG'] and runlist.validate_char(\
            platform_to_post,tweet):
            log.info("""Post exceeded character count for {}. Skipping posts that are
too long is enabled in the config. Skipping.""".format(platform_to_post))
    else:
        print("{} failed to post. Please ensure your config is correct.".format(platform_to_post))

## Does not actually 'tweet' anything. This tells the program which list item from you text 
## list to send off to the various platforms. It could be named better.
def tweet_it():
    if options['TYPE'] == "sequential":
        post_content = tweet_types.s_run(parent_dir)
    else:
        post_content = tweet_types.r_run(parent_dir,options['LIST_LOCATION'])
    for i in destinations:
        actually_post(post_content, i)

## This is the main controller and what gets called every time by main(). I don't know what I was thinking
## when I named these functions.
def lets_post():
    #checks where your list is saved and exits if 'sequential' or 'random' is not explicit
    where_list = pull_config('SETUP')['LIST_LOCATION']
    if not (options['TYPE'] == "sequential" or options['TYPE'] == "random"):
        print("""
        You need to choose the order in which the list will run
        Please edit the config file in config.yaml
        """)
        sys.exit()
    else:
        pass
    if os.path.isfile(where_list):
        pass
    else:
        if connection_validator(where_list) == 200:
            pass
        else:
            error_msg = """There's an issue with your list file. Either the server couldn't connect
to the webpage or the file doesn't exist. Please fix this and run again."""
            print(error_msg)
            log.info(error_msg)
            sys.exit()
    #if there isn't a numbering file in place and you want sequential tweets
    #this makes a number file
    if not os.path.isfile(pickle_dir):
        make_pickle()
        log.info("Numbering started and set to zero")
    else:
        pass
    #converts new text list to json
    #reset all numberings
    #checks for Threads token and attempts to generate if it doesn't exist
    if args.initialize:
        runlist.runit()
        make_pickle()
        msg = "Numbering started and list converted."
        log.info(msg)
        try:
            threads_check = pull_config('PLATFORMS')['THREADS']
        except KeyError:
            msg = "Ready to post!"
            log.info(msg)
            sys.exit()
        if threads_check['ENABLE_PLATFORM'] == True:
            threads = Threads()
            if not os.path.isfile(threads.threads_token):
                msg = "Threads token not present. Attempting to generate."
                log.info(msg)
                if threads_check['CODE'] == "":
                    threads_code = input("""The CODE section in config.yaml appears to be empty.
                    Please paste here to continue.
                    Ctrl + C to quit.
                    """)
                elif threads_check['CODE'] != "":
                    threads_code = threads_check['CODE']
                else:
                    log.info("""Something is wrong with your config.yaml formatting. 
                    Please ensure the config is in the format of config.sample.yaml""")
                    sys.exit()
                try:
                    log.info(threads.get_first_threads_token(threads_code))
                except Exception:
                    log.exception("Failed to get Threads token")
            else:
                log.info("""Threads token file exists. 
                This is not a confirmation of validity, just existence.""")
                sys.exit()



    #authenticates and tweets
    if args.post:
        tweet_it()
    if args.add:
        if options['TYPE'] == 'random':
            runlist.append_json(args.yes)
        elif options['TYPE'] == 'sequential':
            runlist.runit()
            msg = "Lines added. Numbering NOT reset."
            log.info(msg)
        else:
            print("Config error: please choose 'random' or 'sequential' posts.")
    elif not(args.post or args.initialize or args.add):
        msg = "Script run without argument. Nothing posted. See --help for details"
        log.info(msg)

def main():
    try:  
        lets_post()
    except Exception:
        print(traceback.format_exc())
        logging.exception("Something went wrong...")

if __name__ == "__main__":
    main()

## TODO: check time and attempt to generate threads token on threads post.