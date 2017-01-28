import sys
sys.path.append('../')

import requests
import json
import bs4
from db import database
import sqlite3

def get_paper_data(paper):
    r = requests.get('http://europepmc.org/abstract/{src}/{ext_id}'.format(src='MED',ext_id=paper))
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    metas = soup('meta')
    date = find_tag(metas, 'citation_publication_date')
    date = '' if not date else date[0]
    title = find_tag(metas, 'citation_title')
    title = '' if not title else title[0]
    author = find_tag(metas, 'citation_author')
    author = '; '.join(author)
    keywords = find_tag(metas, 'citation_keywords')
    keywords = '' if not keywords else keywords[0]
    return {'date': date, 'author': author, 'title': title, 'keywords': keywords}

def find_tag(metas, name):
    out = []
    for meta in metas:
        try:
            if meta['name'] == name:
                out.append(meta['content'])
        except KeyError:
            pass
    return out

def get_citations(paper):
    r = requests.get('http://www.ebi.ac.uk/europepmc/webservices/rest/{src}/{ext_id}/citations/{page}/{pageSize}/{format}'.format(src='MED', ext_id=paper, page=1, pageSize=200, format='JSON'))
    j = json.loads(r.text)
    return [str(cit['id']) for cit in j['citationList']['citation']]

def get_references(paper):
    r = requests.get('http://www.ebi.ac.uk/europepmc/webservices/rest/{src}/{ext_id}/references/{page}/{pageSize}/{format}'.format(src='MED', ext_id=paper, page=1, pageSize=200, format='JSON'))
    j = json.loads(r.text)
    out = []
    if 'referenceList' in j:
        for cite in j['referenceList']['reference']:
            if 'id' in cite:
                out.append(cite['id'])
    return out


if __name__ == '__main__':

    db = database.Database()

    checked_papers = []
    unchecked_papers = ['21296855']

    paper_limit = 30
    count = 0

    while unchecked_papers and (count < paper_limit):
        target_paper = unchecked_papers.pop()
        print('Processing {}'.format(target_paper))


        p = get_paper_data(target_paper)
        citations = get_citations(target_paper)
        references = get_references(target_paper)

        #add target paper to databse
        print(p)
        db.add_paper(target_paper, p['title'], p['author'], p['date'], p['keywords'])
        for citation in citations:
            try:
                db.add_connection(target_paper, citation)
            except sqlite3.IntegrityError:
                print('UNIQUE constraint failed: ({}, {})'.format(target_paper, citation))
        for reference in references:
            try:
                db.add_connection(reference, target_paper)
            except sqlite3.IntegrityError:
                print('UNIQUE constraint failed: ({}, {})'.format(target_paper, citation))


        for next_paper in citations+references:
            if (next_paper not in checked_papers) or (next_paper not in unchecked_papers):
                unchecked_papers.append(next_paper)
        checked_papers.append(target_paper)
        count += 1
