import sys
sys.path.append("../back_end/db")
sys.path.append("../back_end")

import read_graph
import recommend_papers

import database

#citation_graph = read_graph.read_cit_HepPh()
db = database.Database()
citation_graph = db.get_citation_network()
citation_graph = read_graph.add_first(citation_graph)
#citation_graph = read_graph.add_second(citation_graph)

print(len(citation_graph.nodes()))
print(citation_graph.nodes(data=True))

n_steps=30
paper1="Worcester, MA"
paper2=paper1

#for i in range(n_steps):
#    paper2=list(citation_graph[paper2].keys())[0]

#print(citation_graph.nodes())
#print(recommend_papers.get_papers(citation_graph, paper1, paper2, 1))