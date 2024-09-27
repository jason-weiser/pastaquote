import requests
import os
import logging
import yaml

def log_this(input_for_log):
    ## Logging
    logging_file = '../data/bot.log'
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
    with open("./config.yaml") as config_yml:
        config = yaml.safe_load(config_yml)
    return config[section]
