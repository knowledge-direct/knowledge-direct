# Knowledge Direct

A web app to find you the shortest research path, from your read papers to a target paper, displayed as a graph.

## Getting Started

First initialise the database:
```bash
sh back_end/db/init.sh
```

Install dependencies using (note: Python 3 and pip3 is required):
```bash
pip3 install -r requirements.txt
```

Run the server:
```bash
python3 back_end/server.py
```

## Suggested Things
* knowescape.org
* Neo4j
* dependence tree (rather than relation network)
