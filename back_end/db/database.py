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
                INSERT INTO papers(id, title, author, date)
                VALUES (?, ?, ?, ?);
            """, (title, author, date))
        self.conn.commit()

    def add_connection(self, citing, cited):
        self.curs.execute("""
            INSERT INTO connections(paper_one, paper_two, citing, weight)
            VALUES (?, ?, ?, 0);
        """, (citing, cited, True))
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

    def update_connection(self, citing, cited, **kwargs):
        for key in kwargs:
            self.curs.execute("""
                UPDATE connections SET {}=? WHERE paper_one=? and paper_two=?;
            """.format(key), (kwargs[key], citing, cited))


    def get_network_with_nodes(self):
        citation_graph = nx.Graph()
        self.curs.execute("""
            SELECT id, title, author, date, key_words FROM papers;
            """)
        results = self.curs.fetchall()
        for identifier, title, author, date, key_words in results:
            citation_graph.add_node(identifier, title=title, author=author, date=date, key_words=key_words)
        return citation_graph

    def get_citation_network(self):
        citation_graph = get_network_with_nodes(self)
        self.curs.execute("""
            SELECT paper_one, paper_two FROM connections WHERE citing>0;
            """, args)
        results = self.curs.fetchall()
        for p1, p2 in results:
            if citation_graph.has_node(p1) and citation_graph.has_node(p2):
                citation_graph.add_edge(p1, p2)
        return citation_graph

    def get_weight_network(self, max_weight=None):
        citation_graph = get_network_with_nodes(self)
        self.curs.execute("""
            SELECT paper_one, paper_two, weight FROM connections
            """, args)
        results = self.curs.fetchall()
        for p1, p2, weight in results:
            if citation_graph.has_node(p1) and citation_graph.has_node(p2):
                if max_weight is None: 
                    citation_graph.add_edge(p1, p2, weight=weight)
                else:
                    if weight < max_weight:
                        citation_graph.add_edge(p1, p2, weight=1)
                    else:
                        citation_graph.add_edge(p1, p2, weight=1+(weight-max_weight)*config.DIFFICULT_PAPER_MULTIPLIER)
        return citation_graph


    def list_papers(self, query='', args=[], page_size=None, page=0):
        limit = ''
        if page_size is not None:
            args.append(page_size*page)
            args.append(page)
            limit = 'LIMIT ?, ?'
        self.curs.execute("""
            SELECT * FROM papers {} {};
            """.format(query, limit), args)
        results = self.curs.fetchall()
        return [{'paper_id': res[0], 'title': res[1], 'author': res[2], 'date': res[3], 'key_words': res[4]} for res in results]

    def list_papers_list(self, paper_list, page_size=None, page=0):
        ret = []
        for paper in paper_list:
            ret += list_papers(self, query="""AS p WHERE p.id=?""",
                                 args=[paper_list,], page_size=page_size, page=page)
        return ret




    def list_papers_read(self, user, page_size=None, page=0):
        return self.list_papers(query="""AS p WHERE p.id IN (SELECT paper FROM familiarities WHERE user=? AND value > 0)""",
                             args=[user,], page_size=page_size, page=page)

    def list_papers_unread(self, user, page_size=None, page=0):
        return self.list_papers(query="""AS p WHERE p.id NOT IN (SELECT paper FROM familiarities WHERE user=? AND value > 0)""",
                             args=[user,], page_size=page_size, page=page)


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


if __name__ == '__main__':
    db = Database()
