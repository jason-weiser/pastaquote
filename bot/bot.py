import random
import traceback
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


## Find parent directory
running_file = Path(__file__)
current_dir = running_file.resolve().parents[0]
parent_dir = running_file.resolve().parents[1]
pickle_dir = os.path.join(parent_dir, "data/number.p")

## Load the config
options = pull_config('SETUP')

##Define objects

runlist = RunList(parent_dir, options['LIST_LOCATION'])
destinations = ['TWITTER','MASTODON']

## Program run

##This is for the sequential posting, only.
#https://docs.python.org/3/library/pickle.html
def make_pickle():
    initial_num = 0
    pickle.dump(initial_num, open(pickle_dir,"wb"))

def actually_post(tweet,platform_to_post):
    platform_options = pull_config(platform_to_post)
    if platform_to_post == 'TWITTER':
        platform_function = Twitter()
    elif platform_to_post == 'MASTODON':
        platform_function = Masto()
    else:
        log_this("No platform defined")
    if platform_options['ENABLE_PLATFORM'] == True and \
        not platform_options['SKIP_TOO_LONG'] and \
        runlist.validate_char(platform_to_post,tweet) == 0:
        log_this("Post attempted: {}\nResponse: {}" \
            .format(tweet_types.add_hashtags(tweet,\
            platform_to_post), \
            platform_function.post_it(\
            tweet_types.add_hashtags(tweet, platform_to_post))))
    elif platform_options['ENABLE_PLATFORM'] == False:
            log_this("{} not enabled in config. Skipping.".format(platform_to_post))
    elif platform_options['SKIP_TOO_LONG'] and runlist.validate_char(\
            platform_to_post,tweet):
            log_this("""Post exceeded character count for {}. Skipping posts that are
too long is enabled in the config. Skipping.""".format(platform_to_post))
    else:
        print("{} failed to post. Please ensure your config is correct.".format(platform_to_post))

def tweet_it():
    if options['TYPE'] == "sequential":
        post_content = tweet_types.s_run(parent_dir)
        for i in destinations:
            actually_post(post_content, i)
    elif options['TYPE'] == "random":
        post_content = tweet_types.r_run(parent_dir,options['LIST_LOCATION'])
        for i in destinations:
            actually_post(post_content, i)

def lets_post():
    where_list = pull_config('SETUP')['LIST_LOCATION']
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
    if os.path.isfile(options['LIST_LOCATION']):
        pass
    else:
        if connection_validator(options['LIST_LOCATION']) == 200:
            pass
        else:
            error_msg = """There's an issue with your list file. Either the server couldn't connect
to the webpage or the file doesn't exist. Please fix this and run again."""
        print(error_msg)
        log_this(error_msg)
        sys.exit()
    #if there isn't a numbering file in place and you want sequential tweets
    #this makes a number file
    if not os.path.isfile(pickle_dir):
        make_pickle()
        log_this("Numbering started and set to zero")
    else:
        pass
    #converts new text list to json
    #reset all settings
    if args.initialize:
        runlist.runit()
        make_pickle()
        msg = "Numbering started and list converted. Ready to post!"
        print(msg)
        log_this(msg)
    #authenticates and tweets
    if args.post:
        tweet_it()
    if args.add:
        if options['TYPE'] == 'random':
            runlist.append_json(args.yes)
        elif options['TYPE'] == 'sequential':
            runlis.runit()
            log_this("Lines added. Numbering NOT reset.")
        else:
            print("Config error: please choose 'random' or 'sequential' posts.")
    elif not(args.post or args.initialize or args.add):
        print("One argument is required. See --help for details")
        log_this("Script run without argument. Nothing posted.")

def main():
    try:  
        lets_post()
    except Exception:
        print(traceback.format_exc())
        log_this(print(traceback.format_exc()))

if __name__ == "__main__":
    main()