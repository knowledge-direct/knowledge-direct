import sys
sys.path.append("../back_end")
sys.path.append("../back_end/service_algorithms")
sys.path.append("../back_end/db")
sys.path.append("../back_end/corpus_creation")

import matplotlib
import network_analysis_utils
import recommend_papers
import database

#citation_graph = read_graph.read_cit_HepPh()
db = database.Database()
citation_graph = db.get_citation_network()
citation_graph = network_analysis_utils.add_first(citation_graph)
citation_graph = network_analysis_utils.add_second(citation_graph)
citation_graph = network_analysis_utils.add_keyword_overlap(citation_graph)

print(citation_graph.nodes(data = True))
print(citation_graph.edges(data = True))

n_steps=30
paper1="Worcester, MA"
paper2=paper1

#for i in range(n_steps):
#    paper2=list(citation_graph[paper2].keys())[0]

#print(citation_graph.nodes())
#print(recommend_papers.get_papers(citation_graph, paper1, paper2, 1))