import requests
import os
import logging
import yaml
from pathlib import Path

## Find parent directory
running_file = Path(__file__)
current_dir = running_file.resolve().parents[0]
parent_dir = running_file.resolve().parents[1]

def log_this(input_for_log):
    ## Logging
    logging_file = os.path.join(parent_dir, 'data/bot.log')
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

def connection_validator(url_to_check):
    try:
        response = requests.head(url_to_check)
    except requests.ConnectionError:
        return("Failed to Connect")
    else:
        return response.status_code

def pull_config(section):
    with open(os.path.join(current_dir,'config.yaml')) as config_yml:
        config = yaml.safe_load(config_yml)
    return config[section]
