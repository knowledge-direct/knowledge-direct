import sys
sys.path.append("../")

from db import database
import networkx as nx
import gzip


def calculate_overlap(G, source_paper, target_paper):
    source_edges = set(G[source_paper].keys())
    target_edges = set(G[target_paper].keys())
    overlap_edges = source_edges.intersection(target_edges)  # Number of path of at most 2 - 1
    return len(overlap_edges)

def add_first(G):
    for node1 in G.nodes():
        for node2 in set(G[node1].keys()):
            G[node1][node2]['first_deg'] = 1
    return G


def add_second(G):
    H = G
    for node1 in G.nodes():
        for node2 in set(G[node1].keys()):
            H[node1][node2]['num_second_deg'] = 0

    for node1 in G.nodes():
        for node2 in set(G[node1].keys()):
            for node3 in set(G[node2].keys()):
                if not H.has_edge(node1, node3):
                    H.add_edge(node1, node3, first_deg=0, num_second_deg=0)
                if not G.has_edge(node1, node3):
                    H[node1][node3]['num_second_deg'] += 1
                    print('here')
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
