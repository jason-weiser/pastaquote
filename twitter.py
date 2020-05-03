import dotenv
import os
from requests_oauthlib import OAuth1Session

dotenv.load_dotenv('.env')


class Twitter:
    base_url = 'https://api.twitter.com/'

    def __init__(self):
        self.consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        self.consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
        self.access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        self.session = OAuth1Session(self.consumer_key,
                        client_secret=self.consumer_secret,
                        resource_owner_key=self.access_token,
                        resource_owner_secret=self.access_token_secret)

    def post_tweet(self, status):
        url = "{}1.1/statuses/update.json".format(self.base_url)
        resp = self.session.post(url, {'status': status})
        print(resp.status_code)

twitter = Twitter()

twitter.post_tweet(tweet)


