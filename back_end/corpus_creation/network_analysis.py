import sys
sys.path.append("../")

from db import database
from collections import defaultdict
import networkx as nx
import gzip


def add_first(G):
    for node1 in G.nodes():
        for node2 in G.neighbors(node1):
            G[node1][node2]['first_deg'] = 1
    return G


def add_second(G):
    H = G

    for node1 in G.nodes():
        for node2 in G.neighbors(node1):
            for node3 in G.neighbors(node2):
                if node1 != node3 and not G.has_edge(node1, node3):
                    if not H.has_edge(node1, node3):
                        H.add_edge(node1, node3, num_second_deg=0)
                    H[node1][node3]['num_second_deg'] += 1
    return H



if __name__ == '__main__':

    db = database.Database()
    citation_graph = db.get_citation_network()
    citation_graph = add_first(citation_graph)
    citation_graph = add_second(citation_graph)

    #Write first and second to database
    for node1 in citation_graph:
        for node2 in set(citation_graph[node1].keys()):
            db.update_connection(node1, node2, **citation_graph[node1][node2])
