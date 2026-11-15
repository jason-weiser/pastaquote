import requests
import os
import logging
import yaml
from pathlib import Path

## Find different files
running_file = Path(__file__)
current_dir = running_file.resolve().parents[0]
parent_dir = running_file.resolve().parents[1]
pickle_dir = os.path.join(parent_dir, "data/number.p")

def setup_logging(data_directory):
    log_path = os.path.join(data_directory, "bot.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format ='%(asctime)s : %(levelname)s : %(name)s : %(message)s',
        filename=log_path,
        filemode='a',
    )

def connection_validator(url_to_check):
    try:
        response = requests.head(url_to_check,
        headers={"User-Agent": "Mozilla/5.0"}, 
        stream=True, 
        allow_redirects=True
        )
    except requests.RequestException:
        return 0
    else:
        return response.status_code