from pathlib import Path
import yaml
import os
from mastodon import Mastodon
from requests_oauthlib import OAuth1Session

## Define directories and open up config.yaml
current_d = Path(__file__)
parent_d = current_d.resolve().parents[1]
with open(os.path.join(parent_d, 'data/config.yaml')) as config_yml:
    config = yaml.safe_load(config_yml)
twitter_cred = config['TWITTER']
mastodon_cred = config['MASTODON']
#dotenv.load_dotenv(os.path.join(parent_d, 'data/config.ini'), override=True)


## What makes the magic happen re: tweets
class Twitter:
    base_url = 'https://api.twitter.com/'

    def __init__(self):
        self.consumer_key = twitter_cred['TWITTER_CONSUMER_KEY']
        self.consumer_secret = twitter_cred['TWITTER_CONSUMER_SECRET']
        self.access_token = twitter_cred['TWITTER_ACCESS_TOKEN']
        self.access_token_secret = twitter_cred['TWITTER_ACCESS_TOKEN_SECRET']
        self.session = OAuth1Session(self.consumer_key,
                        client_secret=self.consumer_secret,
                        resource_owner_key=self.access_token,
                        resource_owner_secret=self.access_token_secret)

    def post_tweet(self, status):
        parameters = {
            'status': status
        }

        url = "{}1.1/statuses/update.json".format(self.base_url)
        resp = self.session.post(url, params = parameters)
        return resp.status_code

## What makes the magic happen re:toots
class Masto:
    def __init__(self):
        self.masto = Mastodon(access_token=mastodon_cred['MASTO_ACCESS_TOKEN'], \
            api_base_url=mastodon_cred['MASTO_BASE_URL'])

    def tootit(self, status):
        return self.masto.toot