import networkx as nx
import gzip

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
            citation_graph.add_nodes_from([node1, node2]) # nodes are a set, duplicates are dealt with
            citation_graph.add_edge(node1, node2)

    return(citation_graph)