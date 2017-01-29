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
        cost = nx.shortest_path_length(G, source_paper, target_paper, weight=weight)
        if cost < current_cost:
            papers_in_path_id = get_shortest_path_papers(G, source_paper, target_paper, config.MAX_STEP_SIZE)
            papers_in_path = db.list_papers_list(papers_in_path_id.reverse())
    return papers_in_path
    
def get_shortest_path_papers(G, source_paper, target_paper, max_step_size):
    whole_path = nx.shortest_path(G, source_paper, target_paper, weight=weight)
    papers_in_path=[]
    papers_in_path.append(source_paper)
    differences=[]
    cum_weights = 0

    # This takes the biggest step below the max_step_size
    for i in range(1,len(whole_path)):
        node1 = whole_path[i-1]
        node2 = whole_path[i]
        this_weight = G[node1][node2]['weight']
        differences.append(this_weight)
        print(node1, node2, G[node1][node2]['second'])
        cum_weights += this_weight
        if cum_weights > max_step_size:
            print(cum_weights - this_weight, node1)
            cum_weights = this_weight
            papers_in_path.append(node1)

    papers_in_path.append(target_paper)
    return(papers_in_path)
