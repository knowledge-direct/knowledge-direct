import sys
import requests
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

    def add_familiar(self, user_id, paper_id, value=1):
        self.curs.execute("""
            INSERT INTO familiarities(user, paper, value)
            VALUES (?, ?, ?);
        """, (user_id, paper_id, value))
        self.conn.commit()

    def remove_familiar(self, user_id, paper_id):
        self.curs.execute("""
            DELETE FROM familiarities WHERE user=? AND paper=?;
        """, (user_id, paper_id))
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
            if citation_graph.has_node(p1) and citation_graph.has_node(p2):
                citation_graph.add_edge(p1, p2)
        return citation_graph


    def list_papers(self, page_size=None, page=0):
        if page_size is None:
            self.curs.execute("""
                SELECT * FROM papers;
                """)
        else:
            self.curs.execute("""
                SELECT * FROM papers LIMIT ?, ?;
                """, (page_size*page, page_size))
        results = self.curs.fetchall()
        return [{'paper_id': res[0], 'title': res[1], 'author': res[2], 'date': res[3], 'key_words': res[4]} for res in results]


    def list_papers_read(self, user, page_size=None, page=0):
        if page_size is None:
            self.curs.execute("""
                SELECT * FROM familiarities AS f JOIN papers AS p on f.paper=p.id WHERE f.user=? AND f.value > 0;
                """, (user,))
        else:
            self.curs.execute("""
                SELECT * FROM familiarities AS f JOIN papers AS p on f.paper=p.id WHERE f.user=? AND f.value > 0 LIMIT ?, ?;
                """, (user, page_size*page, page_size))

        results = self.curs.fetchall()
        return [{'paper_id': res[3], 'title': res[4], 'author': res[5], 'date': res[6], 'key_words': res[7]} for res in results]

    def list_papers_unread(self, user, page_size=None, page=0):
        if page_size is None:
            self.curs.execute("""
                SELECT * FROM papers as p WHERE p.id NOT IN (SELECT paper FROM familiarities WHERE user=? AND value > 0);
                """, (user,))
        else:
            self.curs.execute("""
                SELECT * FROM papers as p WHERE p.id NOT IN (SELECT paper FROM familiarities WHERE user=? AND value > 0) LIMIT ?, ?;
                """, (user, page_size*page, page_size))
        results = self.curs.fetchall()
        return [{'paper_id': res[0], 'title': res[1], 'author': res[2], 'date': res[3], 'key_words': res[4]} for res in results]

    # Method for checking if a user exists, if not then creating a new record
    # followed by returning the user's ID
    def create_or_update_user(self, google_id, google_token):
        # Get a new cursor, and select the first row from the query
        t = (str(google_id),)
        self.curs.execute('SELECT id FROM users WHERE id=?', t)
        row = self.curs.fetchone()
        # Check if a row was returned
        if row == None:
            # Send a request to Google to get the user's name
            r = requests.get('https://www.googleapis.com/plus/v1/people/me?access_token=' + google_token)
            # Get the name from the response, ready to insert
            t = (r.json()['displayName'], str(google_id))
            # Insert into the DB
            self.curs.execute('INSERT INTO users (name, id, admin) VALUES (?, ?, 0)', t)
            # Return the ID
            return google_id
        else:
            # Return the ID
            return row[0]


    # Get the name of the user from the database, given their ID
    def get_user_name(self, user_id):
        t = (user_id,)
        self.curs.execute('SELECT name FROM users WHERE id=?', t)
        row = self.curs.fetchone()
        if row == None:
            # Not found, return the empty string
            return ''
        else:
            return row[0]
