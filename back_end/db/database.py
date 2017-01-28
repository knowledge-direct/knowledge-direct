import sys
import networkx as nx
sys.path.append('../')

import sqlite3

import config


class Database:
    def __init__(self, db_addr=config.DB_ADDR):
        self.db_addr = db_addr
        self.conn = sqlite3.connect(self.db_addr)
        self.curs = self.conn.cursor()

    def __del__(self):
        self.conn.close()


    def add_paper(self, key, title, author, date, keywords=None):
        if keywords is not None:
            self.curs.execute("""
                INSERT INTO papers(id, title, author, date, key_words)
                VALUES (?, ?, ?, ?, ?);
            """, (key, title, author, date, keywords))
        else:
            self.curs.execute("""
                INSERT INTO papers(id, title, author, date
                VALUES (?, ?, ?, ?);
            """, (title, author, date))
        self.conn.commit()

    def add_connection(self, citing, cited, value=1):
        self.curs.execute("""
            INSERT INTO connections(citing, cited, value)
            VALUES (?, ?, ?);
        """, (citing, cited, value))
        self.conn.commit()


    def get_citation_network(self):
        citation_graph = nx.Graph()
        self.curs.execute("""
            SELECT id, title, author, date, key_words FROM papers;
            """)
        results = self.curs.fetchall()
        for id, title, author, date, key_words in results:
            citation_graph.add_node(id, title=title, author=author, date=date, key_words=key_words)

        self.curs.execute("""
            SELECT citing, cited FROM connections;
            """)
        results = self.curs.fetchall()
        for p1, p2 in results:
            citation_graph.add_edge(p1, p2)
        return citation_graph
