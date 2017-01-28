import read_graph
import recommend_papers

citation_graph = read_graph.read_cit_HepPh()
citation_graph = read_graph.add_overlap(citation_graph)
print("Graph read")

n_steps=30
paper1="9907233"
paper2=paper1

for i in range(n_steps):
    paper2=list(citation_graph[paper2].keys())[4]

#print(citation_graph.nodes())
print(recommend_papers.get_papers(citation_graph, paper1, paper2, 1))