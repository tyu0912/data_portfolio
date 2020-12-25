import os
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

print(tweepy.__version__)

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=os.getenv('Twitter_API_Key')
consumer_secret=os.getenv('Twitter_API_Secret_Key')

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=os.getenv('Twitter_Access_Token')
access_token_secret=os.getenv('Twitter_Token_Secret')

class MyStreamListener(StreamListener):

    def on_status(self, status):
        print(status.text)
        return status.text

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

if __name__ == '__main__':
    l = MyStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['healthcare'])

    
    # stream.filter(track=['basketball'], follow='19923144')