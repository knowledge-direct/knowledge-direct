import sys
sys.path.append("../back_end")
sys.path.append("../back_end/service_algorithms")
sys.path.append("../back_end/db")
sys.path.append("../back_end/corpus_creation")

import matplotlib
import network_analysis
import keyword_analysis
import recommend_papers
import database

DB_ADDR = '../back_end/db/database.db'

#citation_graph = read_graph.read_cit_HepPh()
db = database.Database()
citation_graph = db.get_citation_network()
citation_graph = network_analysis.add_first(citation_graph)
citation_graph = network_analysis.add_second(citation_graph)
citation_graph = keyword_analysis.add_keyword_overlap(citation_graph)
citation_graph = network_analysis.add_weights(citation_graph, [1,1,1])

#print(citation_graph.nodes(data = True))
#print(citation_graph.edges(data = True))

paper1=list(citation_graph.nodes())[0]
paper2=list(citation_graph.nodes())[29]
print(citation_graph.node[paper1]['title'])
print(citation_graph.node[paper2]['title'])
print(recommend_papers.get_shortest_path_papers(citation_graph, paper1, paper2, 1))