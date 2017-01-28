import sys
sys.path.append("../")

import network_analysis_utils
import recommend_papers
import database

db = database.Database()
citation_graph = db.get_citation_network()
citation_graph = network_analysis_utils.add_first(citation_graph)
citation_graph = network_analysis_utils.add_second(citation_graph)

#Write first and second to database
