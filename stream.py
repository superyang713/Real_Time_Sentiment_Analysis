import credentials
import tweepy


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
        print(status.text)

    def on_error(self, status_code):
        """
        Stop data scraping when it exceeds the rate limits.
        """
        if status_code == 420:
            return False
