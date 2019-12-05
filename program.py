import tweepy
import settings
import credentials
from stream import MyStreamListener


auth = tweepy.OAuthHandler(
    credentials.API_KEY,
    credentials.API_SECRECT_KEY
)
auth.set_access_token(
    credentials.ACCESS_TOKEN,
    credentials.ACCESS_TOKEN_SECRECT
)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(
    auth=api.auth,
    listener=myStreamListener
)
myStream.filter(
    languages=settings.languages,
    track=settings.tracking
)
