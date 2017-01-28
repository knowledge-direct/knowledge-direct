import networkx as nx
import gzip
import re
from collections import defaultdict

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
                    H.add_edge(node1, node3)
                if not G.has_edge(node1, node3):
                    H[node1][node3]['second'] += 1
    return H

# Note: compares everything, makes it into a full graph
def add_keyword_overlap(G):
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 != node2:
                n_overlaps = measure_keyword_overlap(G, node1, node2)
                if n_overlaps > 0:
                    if not G.has_edge(node1, node2):
                        G.add_edge(node1, node2)
                    if not 'keyword_overlap' in G[node1][node2].keys():
                        G[node1][node2]['keyword_overlap'] = n_overlaps
    return G

def measure_keyword_overlap(G, node1, node2):
    list1 = set(re.split("[; ]", G.node[node1]['key_words']))
    list2 = set(re.split("[; ]", G.node[node2]['key_words']))
    overlap_measure = 0.0

    keyword_weights = calculate_keyword_weights(G)

    for word1 in list1:
        for word2 in list2:
            if word1 == word2:
                overlap_measure += keyword_weights[word1]
    return overlap_measure

def calculate_keyword_weights(G):
    key_word_weights = defaultdict(float)

    for node in G.nodes():
        key_words = set(re.split("[; ]", G.node[node]['key_words']))
        for key_word in key_words:
            key_word_weights[key_word] += 1

    for key_word in key_word_weights.keys():
        key_word_weights[key_word] = 1/key_word_weights[key_word]
        
    return key_word_weights