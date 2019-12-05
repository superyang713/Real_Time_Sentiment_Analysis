import tweepy

import credentials
import settings
from database import Connection
from nlp import clean_text, analyze_sentiment


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
        text = clean_text(status.text)
        sentiment = analyze_sentiment(text)
        user_location = status.user.location

        insert_sql = """
        INSERT INTO {}
        (id_str, created_at, text, sentiment, user_location)
        VALUES (%s, %s, %s, %s, %s)
        """.format(settings.table_name)

        val = (id_str, created_at, text, sentiment, user_location)

        with Connection() as db:
            db.create_table_if_not_existed(settings.table_name)
            db.execute(insert_sql, val)

    def on_error(self, status_code):
        """
        Stop data scraping when it exceeds the rate limits.
        """
        if status_code == 420:
            return False
