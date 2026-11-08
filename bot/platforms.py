from pathlib import Path
import yaml
import os
import requests
from useful_resources import pull_config
from requests_oauthlib import OAuth1Session
from atproto import Client

#define the config
platforms = pull_config("PLATFORMS")
creds = {}
for p in platforms:
    try:
        creds[p] = platforms[p]
    except:
        error_msg = f"{p} is not present in the config. Skipping."
        print(error_msg)

twitter_cred = creds.get('TWITTER')
mastodon_cred = creds.get('MASTODON')
threads_cred = creds.get('THREADS')
bluesky_cred = creds.get('BLUESKY')

print(twitter_cred)
print(bluesky_cred)


## What makes the magic happen re: tweets
class Twitter:
    base_url = 'https://api.twitter.com/'
    twitter_cred = creds.get('TWITTER')

    def __init__(self):
        cred = creds.get('TWITTER')
        if not cred:
            raise ValueError("Twitter credentials not found in config")
        self.consumer_key = (cred['TWITTER_CONSUMER_KEY'])
        self.consumer_secret = (cred['TWITTER_CONSUMER_SECRET'])
        self.access_token = (cred['TWITTER_ACCESS_TOKEN'])
        self.access_token_secret = (cred['TWITTER_ACCESS_TOKEN_SECRET'])
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
    api_url = '{}/api/v1/statuses'.format(mastodon_cred['MASTO_BASE_URL'])

    def post_it(self, status):
        auth = {
            'Authorization': 'Bearer {}'.format(mastodon_cred['MASTO_ACCESS_TOKEN'])
        }
        parameters = {
            'status': status
        }
        resp = requests.post(self.api_url, data=parameters, headers=auth)
        return(resp.status_code)
    
class Bluesky:
    client = Client()
    def post_it(self, status):
        user_name = bluesky_cred['USERNAME']
        password = bluesky_cred['PASSWORD']
        self.client.login(user_name, password)
        self.client.send_post(text=status)