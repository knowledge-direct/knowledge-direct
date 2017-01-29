import sys
sys.path.append("../")


from db import database
import networkx as nx
import gzip

import network_analysis
import config




def calculate_weight(G):
    for node1 in G.nodes():
        for node2 in G.neighbors(node1):
            first = 0 if 'first_deg' not in G[node1][node2] else G[node1][node2]['first_deg']
            second = 0 if 'num_second_deg' not in G[node1][node2] else G[node1][node2]['num_second_deg']
            G[node1][node2]['weight'] = 1/(1.+first*config.FIRST_DEG_WEIGHT + 
                                        second*config.NUM_SECOND_DEG_WEIGHT)
    return G



if __name__ == '__main__':

    db = database.Database()
    citation_graph = db.get_citation_network()
    citation_graph = network_analysis.add_first(citation_graph)
    citation_graph = network_analysis.add_second(citation_graph)
    citation_graph = calculate_weight(citation_graph)

    #Write first and second to database
    for node1 in citation_graph:
        for node2 in set(citation_graph[node1].keys()):
            db.update_connection(node1, node2, **citation_graph[node1][node2])
