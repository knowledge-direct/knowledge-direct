import requests

def get_paper_data(paper):
    pass

def get_citations(paper):
    r = requests.get('http://www.ebi.ac.uk/europepmc/webservices/rest/{src}/{ext_id}/citations/{page}/{format}'.format(src='AGR', ext_id='PMC193660', page=1, format='JSON'))

def get_references(paper):
    pass


if __name__ == '__main__':


checked_papers = []
unchecked_papers = ['']

paper_limit = 3000
count = 0

while unchecked_papers or count > paper_limit
    target_paper = unchecked_papers.pop()

    checked_papers.append(get_paper_data(target_paper))

    citations = get_citations(target_paper)
    references = get_references(target_paper)

    for next_paper in citations+references:
        if (next_paper not in checked_papers) or (next_paper not in unchecked_papers):
            unchecked_papers.append(citation)
    count += 1
