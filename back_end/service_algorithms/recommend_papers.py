import sys
sys.path.append('../')

import networkx as nx

import config

def get_shortest_path_recommendation(db, user, target_paper):
    G = db.get_citation_network()

    source_papers = [p['paper_id'] for p in db.list_papers_read(user)]
    if not source_papers:
        return []
    papers_in_path = []
    current_cost = float('inf')
    for source_paper in source_papers:
        cost = nx.shortest_path_length(G, source_paper, target_paper)
        if cost < current_cost:
            papers_in_path_id = nx.shortest_path(G, source_paper, target_paper)
            papers_in_path_id.reverse()
            papers_in_path = db.list_papers_list(papers_in_path_id)
    return papers_in_path

def get_shortest_path_recommendation_set(db, user, target_paper_set):
    