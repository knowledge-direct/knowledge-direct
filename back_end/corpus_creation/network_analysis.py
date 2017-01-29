import sys
sys.path.append("../")

from collections import defaultdict
import networkx as nx

from db import database


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


def add_weights(G, coeffs):
    for (u, v, d) in G.edges(data=True):
        d_default = defaultdict(int, d) # Initialization at zero if key not in dict
        #d['weight'] = coeffs[0]*d_default['first_deg'] + coeffs[1]*d_default['n_second_deg'] + coeffs[2]*d_default['keyword_overlap']
        d['weight'] = 1/(d_default['first_deg'] + 0.1*d_default['num_second_deg'] + d_default['keyword_overlap'])
    return G

if __name__ == '__main__':

    db = database.Database()
    citation_graph = db.get_citation_network()
    citation_graph = add_first(citation_graph)
    citation_graph = add_second(citation_graph)

    #Write first and second to database
    for node1 in citation_graph:
        for node2 in set(citation_graph[node1].keys()):
            db.update_connection(node1, node2, **citation_graph[node1][node2])
