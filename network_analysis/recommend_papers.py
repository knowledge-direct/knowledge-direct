import numpy as np
import matplotlib
import read_graph
import networkx as nx

def calculate_overlap(G, source_paper, target_paper):
    source_edges = set(G[source_paper].keys())
    target_edges = set(G[target_paper].keys())
    overlap_edges = source_edges.intersection(target_edges) # Number of path of at most 2 - 1
    prop_overlap = (len(overlap_edges) + 1)/len(source_edges)
    return(prop_overlap)

def get_papers(G, source_paper, target_paper, max_step_size):
    whole_path = nx.shortest_path(G, source_paper, target_paper)

    papers_in_path=[].append(source_paper)
    differences=[]
    cum_weights = 0
    for i in range(1,len(whole_path)):
        node1 = whole_path[i-1]
        node2 = whole_path[i]
        #this_weight=G[node1][node2]['weight']
        this_weight = 1
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

citation_graph=read_graph.read_cit_HepPh()
print("Graph read")

paper1="9907233"
paper2="9804209"

#print(citation_graph.nodes())
print(get_papers(citation_graph, paper1, paper2, 2))
