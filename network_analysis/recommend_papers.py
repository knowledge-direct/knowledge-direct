import numpy as np
import matplotlib
import networkx as nx

def calculate_overlap(G, source_paper, target_paper):
    source_edges = set(G[source_paper].keys())
    target_edges = set(G[target_paper].keys())
    overlap_edges = source_edges.intersection(target_edges) # Number of path of at most 2 - 1
    prop_overlap = (len(overlap_edges) + 1)/len(source_edges)
    return(prop_overlap)

def get_papers(G, source_paper, target_paper, max_step_size):
    whole_path = nx.shortest_path(G, source_paper, target_paper, weight='weight')

    papers_in_path=[]
    differences=[]
    cum_weights = 0
    for i in range(1,len(whole_path)):
        node1 = whole_path[i-1]
        node2 = whole_path[i]
        this_weight=G[node1][node2]['weight']
        differences.append(this_weight)

        cum_weights += this_weight
        if cum_weights > max_step_size:
            print(cum_weights - this_weight, node1)
            cum_weights = this_weight
            papers_in_path.append(node1)

    papers_in_path.append(target_paper)
    #print(whole_path)
    #print(differences)
    return(papers_in_path)

from tutorial import miles_graph
G=miles_graph()

H = nx.Graph()
for v in G:
    H.add_node(v)
for (u, v, d) in G.edges(data=True):
    if d['weight'] < 300:
        H.add_edge(u, v, weight=1.0)

for (u,v,d) in H.edges(data=True):
    d['weight'] = 1/calculate_overlap(H, u, v)

city1="Sault Sainte Marie, MI"
city2="West Palm Beach, FL"
city3="Valley City, ND"
print(G[city3])
print(H[city3])
#print(calculate_overlap(H, city1, city2, 800))