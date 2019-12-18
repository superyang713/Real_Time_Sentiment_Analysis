import tweepy

import credentials
import settings
from database import Connection
from nlp import preprocess_text, analyze_sentiment, PreProcessTweets
from model import extract_features
import pickle


f = open('./data/classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()


class MyStreamListener(tweepy.StreamListener):
    """
    Twitter stream object.
    It contains all the logics about how to stream tweets.
    """
    def on_status(self, status):
        """
        Storing streaming tweets in the SQL database.
        The returned status object has all the information about a tweet.
        """
        # Exclude all retweets.
        if status.retweeted or 'RT @' in status.text:
            return True

        id_str = status.id_str
        created_at = status.created_at
        text = status.text
        user_location = status.user.location

        tweet = {
            "text": text,
            "label": None
        }
        tweet_processor = PreProcessTweets()
        processed_tweet = tweet_processor.process_tweets([tweet])
        polarity = classifier.classify(extract_features(processed_tweet[0]))
        print(polarity)
        print(processed_tweet)
        print(extract_features(processed_tweet[0]))

        insert_sql = """
        INSERT INTO {}
        (id_str, created_at, text, polarity, user_location)
        VALUES (%s, %s, %s, %s, %s)
        """.format(settings.table_name)

        val = (id_str, created_at, text, polarity, user_location)

        with Connection() as db:
            db.create_table_if_not_existed(settings.table_name)
            db.execute(insert_sql, val)

    def on_error(self, status_code):
        """
        Stop data scraping when it exceeds the rate limits.
        """
        if status_code == 420:
            return False
