from pathlib import Path
import dotenv
import os
from mastodon import Mastodon
from requests_oauthlib import OAuth1Session


current_d = Path(__file__)
parent_d = current_d.resolve().parents[1]
dotenv.load_dotenv(os.path.join(parent_d, 'data/.env'), override=True)



class Twitter:
    base_url = 'https://api.twitter.com/'

    def __init__(self):
        self.consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
        self.consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
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

class Masto:
    base_url = os.getenv('MASTO_BASE_URL')

    def __init__(self):
        self.masto = Mastodon(os.getenv('MASTO_ACCESS_TOKEN'),\
            os.getenv('MASTO_BASE_URL'))

    def tootit(self, status):
        return self.masto(status)