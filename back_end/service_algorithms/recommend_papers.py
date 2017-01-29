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

    additional_nodes = set(G.nodes())
    for paper in papers_in_path_id:
        additional_nodes.remove(paper)

    return (papers_in_path, G.edges(), list(additional_nodes))

def get_shortest_path_recommendation_set(db, user, target_papers):
    G = db.get_citation_network()
    source_papers = [p['paper_id'] for p in db.list_papers_read(user)]
    if not source_papers:
        return []
    # Create contracted graph
    G_contracted = G
    for i in range(len(source_papers)):
        for j in range(i):
            node1 = source_papers[i]
            node2 = source_papers[j]
            if not G.has_edge(node1, node2):
                G_contracted.add_edge(node1, node2)
            G_contracted[node1][node2]['weight'] = 0.0

    # Construct metric closure
    G_metric_closure = nx.Graph()
    nodes_list = target_papers
    for i in range(len(nodes_list)):
        node1 = nodes_list[i]
        G_metric_closure.add_node(node1)
        for j in range(i):
            node2 = nodes_list[j]
            G_metric_closure.add_node(node2)

            this_weight = nx.shortest_path_length(G_contracted, node1, node2)
            path_list = nx.shortest_path(G_contracted, node1, node2)
            G_metric_closure.add_edge(node1, node2, weight=this_weight, path_list=path_list)

    # Add known set
    known_set_label = 'known'
    G_metric_closure.add_node(known_set_label)
    for target_paper in target_papers:
        G_metric_closure.add_node(target_paper)
        (this_weight,closest_source) = get_shortest_path_from_set(G_contracted, source_papers, target_paper)
        path_list = nx.shortest_path(G, closest_source, target_paper)
        G_metric_closure.add_edge(known_set_label, target_paper, weight=this_weight, path_list=path_list)

    # Get minimal spanning tree and traverse it from known
    min_tree = nx.minimum_spanning_tree(G_metric_closure)
    papers_in_path_id = []

    next_set = set()
    next_set.add(known_set_label)
    to_visit = set(min_tree.nodes())

    while len(to_visit) > 0:
        current_set = next_set
        next_set = set()
        for node in current_set:
            to_visit.remove(node)
            for neighbour in min_tree.neighbors(node):
                if neighbour in to_visit:
                    next_set.add(neighbour)
                    path_to_add = G_metric_closure[node][neighbour]['path_list']
                    papers_in_path_id = add_paper_to_path(papers_in_path_id, path_to_add, source_papers)

    papers_in_path_id.reverse()
    papers_in_path = db.list_papers_list(papers_in_path_id)

    additional_nodes = set(G.nodes())
    for paper in papers_in_path_id:
        additional_nodes.remove(paper)

    return (papers_in_path, G.edges(), list(additional_nodes))

def add_paper_to_path(papers_in_path_id, path_to_add, source_papers):
    for node in path_to_add:
        if not node in papers_in_path_id and node not in source_papers:
            papers_in_path_id.append(node)
    return papers_in_path_id

def get_shortest_path_from_set(G, source_papers, target_paper):
    cost = float('inf')
    for source_paper in source_papers:
        current_cost = nx.shortest_path_length(G, source_paper, target_paper)
        if current_cost < cost:
            cost = current_cost
            closest_source = source_paper
    return (cost, closest_source)