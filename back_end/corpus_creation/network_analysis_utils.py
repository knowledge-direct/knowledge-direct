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
            G[node1][node2]['first'] = 1
    return G


def add_second(G):
    H = G
    for node1 in G.nodes():
        for node2 in set(G[node1].keys()):
            H[node1][node2]['second'] = 0

    for node1 in G.nodes():
        for node2 in set(G[node1].keys()):
            for node3 in set(G[node2].keys()):
                if not H.has_edge(node1, node3):
                    H.add_edge(node1, node3, first=0, second=0)
                if not G.has_edge(node1, node3):
                    H[node1][node3]['second'] += 1
    return H
