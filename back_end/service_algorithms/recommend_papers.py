import sys
sys.path.append('../')

import networkx as nx

import config

def get_shortest_path_recommendation(db, user, target_paper):
    G = db.get_citation_network()

    source_papers = [p['paper_id'] for p in db.list_papers_read(user)]
    if not source_papers:
        return []

    (min_cost, closest_source) = get_shortest_path_from_set(G, source_papers, target_paper)
    papers_in_path_id = nx.shortest_path(G, closest_source, target_paper)
    papers_in_path_id.reverse()
    papers_in_path = db.list_papers_list(papers_in_path_id)
    return papers_in_path

def get_shortest_path_recommendation_set(db, user, target_papers):
    G = db.get_citation_network()

    source_papers = [p['paper_id'] for p in db.list_papers_read(user)]
    if not source_papers:
        return []
    papers_in_path_id = []

    # Construct metric closure
    G_metric_closure = nx.Graph()
    known_set_label = 'known'
    G_metric_closure.add_node(known_set_label)
    for target_paper in target_papers:
        G_metric_closure.add_node(target_paper)
        this_weight = get_shortest_path_from_set(G, source_set, target_paper)
        G_metric_closure.add_edge(known_set_label, target_paper, weight=this_weight)

    # Print minimal spanning tree from closest target paper
    #minimum_spanning_tree(G_target_papers)

    papers_in_path_id.reverse()
    papers_in_path = db.list_papers_list(papers_in_path_id)
    return papers_in_path

def get_shortest_path_from_set(G, source_papers, target_paper):
    cost = float('inf')
    for source_paper in source_papers:
        current_cost = nx.shortest_path_length(G, source_paper, target_paper)
        if current_cost < cost:
            cost = current_cost
            closest_source = source_paper
    return (cost, closest_source)