import requests
import os
import logging
from pathlib import Path

def connection_validator(url_to_check):
    try:
        response = requests.head(url_to_check)
    except requests.ConnectionError:
        return("Failed to Connect")
    else:
        return response.status_code

        ##TODO: Add logging to this file

def log_this(input_for_log):
## Find parent directory
    running_file = Path(__file__)
    current_dir = running_file.resolve().parents[0]
    parent_dir = running_file.resolve().parents[1]

    ## Logging

    logging_file = os.path.join(parent_dir, 'data/twitterbot.log')
    if not os.path.isfile(logging_file):
        log_file = open(logging_file, 'x')
        log_file.close()

    logging.basicConfig(
        level=logging.INFO,
        format ='%(asctime)s : %(levelname)s : %(message)s',
        filename=logging_file,
        filemode='a+',
    )
    logging.info(input_for_log)

log_this("did this log?")