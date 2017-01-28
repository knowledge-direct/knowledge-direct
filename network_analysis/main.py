import sys
sys.path.append("../back_end/db")
sys.path.append("../back_end")

from nltk.corpus import biocreative_ppi

import read_graph
import recommend_papers
import database

citation_graph = read_graph.read_cit_HepPh()
db = database.Database()
citation_graph = db.get_citation_network()
citation_graph = read_graph.add_first(citation_graph)
citation_graph = read_graph.add_second(citation_graph)

#print(citation_graph.nodes(data=True))
node1 = list(citation_graph.nodes())[1]
node2 = list(citation_graph.nodes())[2]

list1 = set(citation_graph.node[node1]['key_words'].split(";"))
list2 = set(citation_graph.node[node2]['key_words'].split(";"))
similarity=dict()

for word1 in list1:
    for word2 in list2:
        wordFromList1 = biocreative_ppi.synsets(word1)
        wordFromList2 = biocreative_ppi.synsets(word2)
        if wordFromList1 and wordFromList2:  # Thanks to @alexis' note
            s = wordFromList1[0].wup_similarity(wordFromList2[0])
            similarity[word1+"_"+word2]=s

print(list1)
print(list2)
print(similarity)

n_steps=30
paper1="Worcester, MA"
paper2=paper1

#for i in range(n_steps):
#    paper2=list(citation_graph[paper2].keys())[0]

#print(citation_graph.nodes())
#print(recommend_papers.get_papers(citation_graph, paper1, paper2, 1))