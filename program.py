import credentials
import tweepy
import MySQLdb

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        """
        Extract info from tweets
        """
        id_str = status.id_str
        created_at = status.created_at
        user_created_at = status.user.created_at

    def on_error(self, status_code):
        """
        Stop data scraping when it exceeds the rate limits.
        """
        if status_code == 420:
            return False


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
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(languages=["en"], track=["Apple"])

db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="gofpdseorkg713",
    database="TwitterDB",
    charset="utf8"
)

if db.is_connected():
    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(TABLE_NAME))
    if mycursor.fetchone()[0] != 1:
        mycursor.execute("CREATE TABLE {} ({})" \
            .format(TABLE_NAME, TABLE_ATTRIBUTES))
        mydb.commit()
    mycursor.close()
