"""
Various helper functions to make life easier.
"""


import pandas as pd

from database import Connection
import settings


def extract_data(table_name):
    sql = """
    SELECT * from {}
    """.format(table_name)
    db = Connection()
    df = pd.read_sql(sql, db.conn)
    return df
