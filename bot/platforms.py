from pathlib import Path
import yaml
import os
import sys
import requests
import logging
from useful_resources import log_this, pull_config, parent_dir, create_file_in_data, print_and_log
from requests_oauthlib import OAuth1Session
from atproto import Client

#logs
log = logging.getLogger(__name__)

#define the config
try:
    platforms = pull_config('PLATFORMS')
except KeyError:
    msg = "Attempting to use old config. Please update config to new format, as this will likely break with future updates."
    print(msg)
    logging.info(msg)
    platforms = None

creds = {}
if not platforms:
    platforms = ['MASTODON','TWITTER','BLUESKY','THREADS']
for p in platforms:
    try:
        creds[p] = platforms[p]
    except:
        msg = f"{p} is not present in the config. Skipping."
        print(msg)
        logging.info(msg)


## What makes the magic happen re: tweets
class Twitter:
    base_url = 'https://api.twitter.com/'

    def __init__(self):
        self.cred = creds.get('TWITTER')
        if not self.cred:
            raise ValueError("Twitter credentials not found in config")
        self.consumer_key = self.cred['TWITTER_CONSUMER_KEY']
        self.consumer_secret = self.cred['TWITTER_CONSUMER_SECRET']
        self.access_token = self.cred['TWITTER_ACCESS_TOKEN']
        self.access_token_secret = self.cred['TWITTER_ACCESS_TOKEN_SECRET']
        self.session = OAuth1Session(self.consumer_key,
                        client_secret=self.consumer_secret,
                        resource_owner_key=self.access_token,
                        resource_owner_secret=self.access_token_secret)

    def post_it(self, status):
        parameters = {
            'text': status
        }

        url = "{}2/tweets".format(self.base_url)
        resp = self.session.post(url, json = parameters)
        return resp.content

## What makes the magic happen re:toots
class Masto:
    def __init__(self):
        self.cred = creds.get('MASTODON')
        self.api_url = '{}/api/v1/statuses'.format(self.cred['MASTO_BASE_URL'])

    def post_it(self, status):
        auth = {
            'Authorization': 'Bearer {}'.format(self.cred['MASTO_ACCESS_TOKEN'])
        }
        parameters = {
            'status': status
        }
        resp = requests.post(self.api_url, data=parameters, headers=auth)
        return(resp.status_code)
    
class Bluesky:
    def __init__(self):
        self.cred = creds.get('BLUESKY')
    client = Client()
    def post_it(self, status):
        user_name = self.cred['USERNAME']
        password = self.cred['PASSWORD']
        self.client.login(user_name, password)
        self.client.send_post(text=status)

class Threads:
    def __init__(self):
        self.cred = creds.get('THREADS')
        self.threads_token = "data/threads_token.json"

    def load_threads_token(self):
        with open(self.threads_token) as f:
            return json.load(f)

    #first-time generation of Threads token, requiring long authorization code. See README.
    def get_first_threads_token(self, code=None):
        if not code:
            code = self.cred.get('CODE')
        if not code:
            code = input("Please paste your code: ").strip()
        if not code:
            raise ValueError("No Threads code provided.")

        r = requests.post("https://graph.threads.net/oauth/access_token", 
            data={
                "client_id": self.cred['APP_ID'],
                "client_secret": self.cred['APP_SECRET'],
                "grant_type": "authorization_code",
                "redirect_uri": self.cred['REDIRECT_URI'],
                "code": code,
            }
        )

        r.raise_for_status()
        shortened_request = r.json()
        print("User ID: {}".format(shortened_request["user_id"]))

        r = requests.get(
            "https://graph.threads.net/access_token", 
            params={
                "grant_type": "th_exchange_token",
                "client_secret": self.cred['APP_SECRET'],
                "access_token": shortened_request["access_token"],
            }
        )
        r.raise_for_status()

        with open(self.threads_token, "w") as f:
            json.dump(
                {
                    "access_token": r.json()["access_token"],
                    "refreshed_at": time.time()
                }, f
            )
        msg = "Saved a long-lived Threads token for the first time. Long Live the Token. "
        return msg


    def save_threads_token(self, token):
        with open(self.threads_token, "w") as f:
            json.dump(
                {
                    "access_token": token,
                    "refreshed_at": time.time()
                }, f
            )
        msg = "New Threads token saved because old one was > 7 days ago. "
        print(msg)
        logging.info(msg)

    def get_valid_threads_token(self):
        th_json_data = load_threads_token()
        age_days = (time.time() - th_json_data["refreshed_at"]) / 86400
        if age_days > 7:
            r = requests.get(
                "https://graph.threads.net/refresh_access_token",
                params={
                    "grant_type": "th_refresh_token",
                    "access_token": th_json_data["access_token"]
                }
            )
            r.raise_for_status()
            save_threads_token(r.json()["access_token"])
            return r.json()["access_token"]
        return th_json_data["access_token"]

    def post_it(self, status):
        threads_url = self.cred['BASE']
        threads_id = self.cred['USER_ID']

        threads_token = load_threads_token()['access_token']
        params = {
            "access_token": threads_token,
            "media_type": "TEXT",
            "text": status
            }
        r = requests.post(
            "{}/{}/threads".format(threads_url,threads_id),params=params)

        msg = f"Threads status code & text: {r.status_code, r.text}"
        print(msg)
        logging.info(msg)
        r.raise_for_status()
        container_id = r.json()["id"]

        r = requests.post("{}/{}/threads_publish".format(threads_url,threads_id),
                            params= {
                                "creation_id": container_id,
                                "access_token": threads_token
                            }
                        )
        r.raise_for_status()
        return r.json()["id"]