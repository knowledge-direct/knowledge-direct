import networkx as nx
import gzip


def calculate_overlap(G, source_paper, target_paper):
    source_edges = set(G[source_paper].keys())
    target_edges = set(G[target_paper].keys())
    overlap_edges = source_edges.intersection(target_edges)  # Number of path of at most 2 - 1
    return len(overlap_edges)

def add_overlap(G):
    for node1 in G.nodes():
        for node2 in set(G[node1].keys()):
            for node3 in set(G[node2].keys()):
                if not G.has_edge(node1, node3):
                    G.add_edge(node1, node3, first=0, second=0)
                G[node1][node3]['second'] += 1
    return G


def read_cit_HepPh():
    graph_file = gzip.open("../../datasets/cit-HepPh.txt.gz", "r")

    citation_graph = nx.Graph()

    for line in graph_file.readlines():
        line = line.decode().strip()
        if line.startswith("#"):  # skip comments
            continue
        else:
            node1 = line.split()[0]
            node2 = line.split()[1]
            citation_graph.add_nodes_from([node1, node2])  # nodes are a set, duplicates are dealt with
            citation_graph.add_edge(node1, node2, first=1, second=0)

    return citation_graph
