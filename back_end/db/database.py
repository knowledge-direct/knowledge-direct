import sys
sys.path.append('../')

import sqlite3

import config


class database:
    def __init__(self, db_addr=config.DB_ADDR):
        self.db_addr = db_addr
        self.conn = sqlite.connect(self.db_addr)
        self.curs = self.conn.cursor()

    def __del__(self):
        self.conn.close()


    def add_paper(self, title, author, abstract, keywords=None):
        if keywords is not None:
            self.curs.execute("""
                INSERT INTO papers
                VALUES (?, ?, ?, ?);
            """, title, author, abstract, keywords)
        else:
            self.curs.execute("""
                INSERT INTO papers
                VALUES (?, ?, ?);
            """, title, author, abstract)
        self.conn.commit()

    def connect_paper(paper1, paper2, value):
        self.curs.execute
