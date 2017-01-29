import sys
sys.path.append("../")

import networkx as nx

import config
from db import database
import network_analysis


def calculate_weight(G):
    for (u, v, d) in G.edges(data=True):
        d_default = defaultdict(int, d)
        #d['weight'] = coeffs[0]*d_default['first_deg'] + coeffs[1]*d_default['n_second_deg'] + coeffs[2]*d_default['keyword_overlap']
        try:
            d['weight'] = 1/(config.FIRST_DEF_WEIGHT*d_default['fsrst_deg']
                             + config.NUM_SECOND_DEG_WEIGHT*d_default['num_second_deg']
                             + config.KEYWORD_OVERLAP_WEIGHT*d_default['keyword_overlap'])
        except ZeroDivisionError:
            G.remove_edge(u,v)
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
