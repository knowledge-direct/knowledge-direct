import sys
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
        self.curs.execute("""
            SELECT (citing, cited) FROM connections;
            """)
        results = self.curs.fetchall()
        citation_graph = nx.Graph()
        for p1, p2 in results:
            citation_graph.add_nodes_from([p1, p2])  # nodes are a set, duplicates are dealt with
            citation_graph.add_edge(p1, p2, is_cited=1)
        return citation_graph
