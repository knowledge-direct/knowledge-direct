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
                INSERT INTO papers(id, title, author, date)
                VALUES (?, ?, ?, ?);
            """, (title, author, date))
        self.conn.commit()

    def add_connection(self, citing, cited):
        self.curs.execute("""
            INSERT INTO connections(paper_one, paper_two, citing)
            VALUES (?, ?, ?);
        """, (citing, cited, True))
        self.conn.commit()

    def update_connection(self, citing, cited, **kwargs):
        for key in kwargs:
            self.curs.execute("""
                UPDATE connections SET {}=? WHERE paper_one=? and paper_two=?;
            """.format(key), (kwargs[key], citing, cited))
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
            SELECT paper_one, paper_two FROM connections WHERE citing=0;
            """)
        results = self.curs.fetchall()
        for p1, p2 in results:
            if citation_graph.has_node(p1) and citation_graph.has_node(p2):
                citation_graph.add_edge(p1, p2)
        return citation_graph


    def list_papers(self, query='', args=[], page_size=None, page=0):
        limit = ''
        if user is not None:
            args.append(user)
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
        return list_papers(self, query="""AS p WHERE p.id IN (SELECT paper FROM familiarities WHERE user=? AND value > 0)""",
                             args=[user,], page_size=page_size, page=page)

    def list_papers_unread(self, user, page_size=None, page=0):
        return list_papers(self, query="""AS p WHERE p.id NOT IN (SELECT paper FROM familiarities WHERE user=? AND value > 0)""",
                             args=[user,], page_size=page_size, page=page)


if __name__ == '__main__':
    db = Database()
