"""
Various helper functions to make life easier.
"""


import pandas as pd
import tweepy

from database import Connection
import credentials
import settings


def extract_data(table_name):
    sql = """
    SELECT * from {}
    """.format(table_name)
    db = Connection()
    df = pd.read_sql(sql, db.conn)
    return df


def connect_api():
    auth = tweepy.OAuthHandler(
        credentials.API_KEY,
        credentials.API_SECRECT_KEY
    )
    auth.set_access_token(
        credentials.ACCESS_TOKEN,
        credentials.ACCESS_TOKEN_SECRECT
    )
    api = tweepy.API(auth)
    return api
