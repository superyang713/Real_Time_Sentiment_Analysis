import MySQLdb

import credentials
import settings

class Connection:

    def __init__(self):
        self.conn = MySQLdb.connect(**credentials.dbc)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.conn.close()

    def query(self, sql, val=None):
        self.cursor.execute(sql, val)
        return self.cursor.fetchall()

    def execute(self, sql, val=None):
        self.cursor.execute(sql, val)

    def commit(self):
        self.conn.commit()

    def create_table_if_not_existed(self, tablename):
        self.execute(
            """
            SELECT count(*)
            FROM information_schema.TABLES
            WHERE TABLE_NAME = '{}';
            """.format(settings.table_name)
        )
        if self.cursor.fetchone()[0] == 0:
            self.execute(
                "CREATE TABLE {} ({});".format(
                    settings.table_name,
                    settings.table_attributes
                )
            )
            self.commit()
        else:
            return
