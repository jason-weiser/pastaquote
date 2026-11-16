import random
import traceback
import json
import pickle
import os
import sys
import argparse
import yaml
import logging
from pathlib import Path
from pastaquote.config import set_config_path, pull_config, platform_config, data_dir
from pastaquote import tweet_types
from pastaquote.useful_resources import connection_validator, parent_dir, setup_logging
from pastaquote.platforms import Masto, Bluesky, Threads
from pastaquote.run_list import RunList

## Arguments for command-line use
parser = argparse.ArgumentParser(
    description='A command line python bot to tweet from a text list'
   )
parser.add_argument('--config','-c', help="location of config.yaml", \
                    dest="config_dest", type=str, action="store")
parser.add_argument('init', 'initialize', help='converts text list, starts numbering', \
                    dest='initialize', action="store_true")
parser.add_argument('post', help="posts the next item in the list", \
                    dest='post', action='store_true')
parser.add_argument('add', help="adds items to running list", \
                    dest='add', action='store_true')
parser.add_argument('check-threads-token', help="refreshes/fetches the Threads token", \
                    dest='threads', action='store_true')
parser.add_argument('-y', help="approve auto-adding", \
                    dest='yes', action='store_true')
args = parser.parse_args()

### Logs
log = logging.getLogger(__name__)

# functions

## This is for the sequential posting only.
# https://docs.python.org/3/library/pickle.html

def make_pickle(p_path):
    initial_num = 0
    pickle.dump(initial_num, open(p_path,"wb"))

## Check to see if threads is enabled/present and, if so, check the token
## if token doesn't exist, it attempts to fetch it based on auth code

def check_threads_token(init=None):
    try:
        threads_check = pull_config('PLATFORMS')['THREADS']
    except KeyError:
        msg = "Threads is not in the config. Skipping."
        log.info(msg)
        return
    if init != "init" and not threads_check.get('ENABLE_PLATFORM'):
        return
    threads = Threads()
    if not os.path.isfile(threads.threads_token):
        msg = "Threads token not present. Attempting to generate."
        log.info(msg)
        threads_code = threads_check.get('CODE')
        if not threads_code:
            threads_code = input("The CODE section in config.yaml appears to be empty. Please paste here to continue. Ctrl + C to quit.\n")
        else:
            threads_code = threads_check['CODE']
        try:
            log.info(threads.get_first_threads_token(threads_code))
        except Exception:
            log.exception("Failed to get Threads token")

## Despite three functions having the word 'post' in them, this is what *actually* posts. It's the last in the line
## and it's what interfaces with the various APIs

def post_with_api(tweet, platform_to_post, data_directory, options):
    runlist = RunList(data_directory, options['LIST_LOCATION'])
    platform_dict = {
        'MASTODON': Masto,
        'BLUESKY': Bluesky,
        'THREADS': Threads
    }
    platform_name = platform_dict.get(platform_to_post)
    if platform_name is None:
        msg = f"Platform ({platform_to_post}) is not a valid platform. Please remove from config. Skipping."
        print(msg)
        log.warning(msg)
        return

    platform_options = pull_config('PLATFORMS')[platform_to_post]
    character_check = runlist.validate_char(platform_to_post, tweet)
    if platform_options['ENABLE_PLATFORM'] and \
        (not platform_options['SKIP_TOO_LONG'] or character_check == 0):
        formatted_post = tweet_types.add_hashtags(tweet, platform_to_post)
        log.info("Attempting post: %s", formatted_post)
        try:
            platform_class = platform_name()
            post_id = platform_class.post_it(formatted_post)
            log.info("%s posted successfully: %s", platform_to_post, post_id)
        except Exception:
            log.exception("%s failed to post.", platform_to_post)
    elif not platform_options['ENABLE_PLATFORM']:
            log.info("{} not enabled in config. Skipping.".format(platform_to_post))
    elif platform_options['SKIP_TOO_LONG'] and character_check == 1:
            log.info("""Post exceeded character count for {}. Skipping posts that are
too long is enabled in the config. Skipping.""".format(platform_to_post))
    else:
        print("{} failed to post. Something went very wrong.".format(platform_to_post))

## This tells the program which list item from you text 
## list to send off to the various platforms. It could be named better.

def choose_post_type(options, data_directory, destinations):
    if options['TYPE'] == "sequential":
        post_content = tweet_types.s_run(data_directory)
    else:
        post_content = tweet_types.r_run(data_directory,options['LIST_LOCATION'])
    for p in destinations:
        post_with_api(post_content, p, data_directory, options)

## This is the main controller and what gets called every time by main(). I don't know what I was thinking
## when I named these functions.

def check_and_route(options, data_directory, destinations):
    runlist = RunList(data_directory, options['LIST_LOCATION'])
    #checks where your list is saved and exits if 'sequential' or 'random' is not explicit
    p_path = Path(data_directory) / "number.p"
    list_location = pull_config('SETUP')['LIST_LOCATION']
    if not (options['TYPE'] == "sequential" or options['TYPE'] == "random"):
        print("""
        You need to choose the order in which the list will run
        Please edit the config file in config.yaml
        """)
        sys.exit()
    if os.path.isfile(list_location):
        pass
    else:
        if connection_validator(list_location) == 200:
            pass
        else:
            error_msg = """There's an issue with your list file. Either the server couldn't connect
to the webpage or the file doesn't exist. Please fix this and run again."""
            print(error_msg)
            log.info(error_msg)
            sys.exit()
    #if there isn't a numbering file in place and you want sequential tweets
    #this makes a number file
    if not os.path.isfile(p_path) and options['TYPE'] == "sequential":
        make_pickle(p_path)
        log.info("Numbering started and set to zero.")
    else:
        pass
    #converts new text list to json
    #reset all numberings
    #checks for Threads token and attempts to generate if it doesn't exist
    if args.initialize:
        runlist.runit()
        if options['TYPE'] == "sequential":
            make_pickle(p_path)
        msg = "List ready for posting."
        log.info(msg)
        check_threads_token(init)
    #authenticates and tweets
    if args.post:
        check_threads_token()
        choose_post_type(options, data_directory, destinations)
    if args.add:
        if options['TYPE'] == 'random':
            runlist.append_json(args.yes)
        elif options['TYPE'] == 'sequential':
            runlist.runit()
            msg = "Lines added. Numbering NOT reset."
            print(msg)
            log.info(msg)
        else:
            print("Config error: please choose 'random' or 'sequential' posts.")
    if args.threads:
        check_threads_token("init")
    elif not(args.post or args.initialize or args.add):
        msg = "Script run without argument. Nothing posted. See --help for details"
        print(msg)
        log.info(msg)

def main():
    if not args.config_dest:
        print("You need to specify a config.yaml. Do so with 'pastaquote --config /path/to/config.yaml'")
        sys.exit()
    try:
        set_config_path(args.config_dest)
        destinations = list(platform_config())
        options = pull_config('SETUP')
        data_path = data_dir()
        setup_logging(data_path) 
        lets_post(options, data_path, destinations)
    except Exception:
        print(traceback.format_exc())
        logging.exception("Something went wrong...")

# TODO: Subprocess updater with argparser
# TODO: single word args (how?)