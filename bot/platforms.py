from pathlib import Path
import yaml
import os
import requests
from useful_resources import pull_config
from requests_oauthlib import OAuth1Session
from atproto import Client

#define the config
mastodon_cred = pull_config('MASTODON')
twitter_cred = pull_config('TWITTER')
bluesky_cred = pull_config('BLUESKY')


## What makes the magic happen re: tweets
class Twitter:
    base_url = 'https://api.twitter.com/'

    def __init__(self):
        self.consumer_key = (twitter_cred['TWITTER_CONSUMER_KEY'])
        self.consumer_secret = (twitter_cred['TWITTER_CONSUMER_SECRET'])
        self.access_token = (twitter_cred['TWITTER_ACCESS_TOKEN'])
        self.access_token_secret = (twitter_cred['TWITTER_ACCESS_TOKEN_SECRET'])
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