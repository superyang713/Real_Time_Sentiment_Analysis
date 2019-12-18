import tweepy
from stream import MyStreamListener

import settings
import credentials
from utils import connect_api


api = connect_api()

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(
    auth=api.auth,
    listener=myStreamListener
)
myStream.filter(
    languages=settings.languages,
    track=settings.tracking
)
