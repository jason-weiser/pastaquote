import random
import traceback
import json
import pickle
import os
import sys
import argparse
import yaml
import logging
import shutil
import subprocess
from importlib.resources import files
from pathlib import Path
from pastaquote.config import set_config_path, pull_config, platform_config, data_dir
from pastaquote import tweet_types
from pastaquote.useful_resources import connection_validator, parent_dir, setup_logging
from pastaquote.platforms import Masto, Bluesky, Threads
from pastaquote.run_list import RunList
DEFAULT_CONFIG = Path.home() / ".config" / "pastaquote"

## Arguments for command-line use
parser = argparse.ArgumentParser(
    description='A command line python bot to post to social media from a text list'
   )
parser.add_argument('--config','-c', help="location of config.yaml", dest="config_dest")
sub = parser.add_subparsers(dest="command", required=True)

setup_p = sub.add_parser('setup', help='converts text list, starts numbering')
setup_p.add_argument('-t', '--token', help="(optional) paste Threads auth token in command line",\
                      dest="token_paste", type=str, action="store")
sub.add_parser('post', help="posts the next item in the list")
sub.add_parser('update', help="Checks and installs updates from Github if you installed via uv.")
add_p = sub.add_parser('add-lines', help="adds items to running list")
add_p.add_argument('-y', '--yes', help="(optional) approve additions to list without review",\
                    action='store_true')
th_token = sub.add_parser('threads-token', help="refreshes/fetches the Threads token")
th_token.add_argument('-t', '--token', help="(optional) paste Threads auth token in command line",\
                      dest="token_paste", type=str, action="store")

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

def check_threads_token(data_directory, init=False, code=None):
    try:
        threads_check = pull_config('PLATFORMS')['THREADS']
    except KeyError:
        msg = "Threads is not in the config. Skipping."
        log.info(msg)
        return
    if init != "init" and not threads_check.get('ENABLE_PLATFORM'):
        return
    threads = Threads(data_directory)
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
            platform_class = platform_name(data_directory)
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

## Pretty self-explanatory. Updates via subprocess. Returns text to print/log

def self_updater():
    msg = "Update attempted via self update."
    print(msg)
    log.info(msg)
    if "uv/tools" not in sys.prefix:
        response = "It seems you didn't install with uv. Please update the way you installed."
        return response
    uv = shutil.which("uv")
    if not uv:
        response = "Couldn't find uv in your path. Update not successful."
        return response
    result = subprocess.run(
        [uv, "tool", "upgrade", "pastaquote"],
        capture_output=True, text=True,
    )
    output = result.stdout + result.stderr
    print(output)
    if result.returncode !=0:
        response = f"Update failed. Return code: {output.returncode}"
    elif "Nothing to upgrade" in output:
        response = "Pastaquote is already up-to-date."
    else:
        response = "Pastaquote updated!"
    return response

## This is the main controller and what gets called every time by main().

def check_and_route(args, options, data_directory, destinations):
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
    if args.command == 'setup':
        runlist.runit()
        if options['TYPE'] == "sequential":
            make_pickle(p_path)
            log.info("Numbering started and set to zero.")
        msg = "List ready for posting."
        log.info(msg)
        check_threads_token(data_directory, init=True, code=args.token_paste)
    #authenticates and tweets
    if args.command == 'post':
        check_threads_token()
        choose_post_type(options, data_directory, destinations)
    if args.command == 'add-lines':
        if options['TYPE'] == 'random':
            runlist.append_json(auto=args.yes)
        elif options['TYPE'] == 'sequential':
            runlist.runit()
            msg = "Lines added. Numbering NOT reset."
            print(msg)
            log.info(msg)
        else:
            print("Config error: please choose 'random' or 'sequential' posts.")
    if args.command == "update":
        update_response = self_updater()
        log.info(update_response)
        print(update_response)
    if args.command == 'threads-token':
        check_threads_token(init=True, code=args.token_paste)

def main():
    args = parser.parse_args()
    sample = files("pastaquote") / "config.sample.yaml"
    default_config_yaml = Path(DEFAULT_CONFIG) / "config.yaml"
    if not args.config_dest and not os.path.exists(default_config_yaml):
        print(f"No config specified. Default config folder does not exist. Creating {DEFAULT_CONFIG}")
        try:
            DEFAULT_CONFIG.mkdir(parents=True, exist_ok=True)
            default_config_yaml.write_text(sample.read_text())
        except Exception as e:
            print(f"Creation of default config directory failed. Please check permissions and try again. Error: {e}")
            raise        
        if os.path.exists(default_config_yaml):
            print("Default directory created.")
            print(f"Please edit the config at {default_config_yaml} and run 'pastaquote setup' again.")
            sys.exit()
        else:
            print("Python didn't throw up an exception when trying to create")
            print(f"a directory at {DEFAULT_CONFIG}, but it still doesn't exist")
            print("Honestly not sure what's going on.")
            sys.exit()
    elif not args.config_dest and os.path.exists(DEFAULT_CONFIG):
        config_location = default_config_yaml
    elif args.config_dest:
        config_location = args.config_dest
    try:
        set_config_path(config_location)
        data_path = data_dir()
        setup_logging(data_path) 
        destinations = list(platform_config())
        options = pull_config('SETUP')
        check_and_route(args, options, data_path, destinations)
    except Exception:
        print(traceback.format_exc())
        log.exception("Something went wrong...")

# TODO: Subprocess updater with argparser