#!/usr/bin/env bash

# Halt on errors
set -e

echo "If the database+table exists already a message to this effect will be
displayed. You may need to delete the database, or check whether it contains
the same information as specified in this script."
read -p "Press enter to continue"

DB="db/database.db"

# Create the database directory
mkdir -p db
# Create the database- ignore errors, hopefully they only occur if the db
# already exists
sqlite3 $DB '
    CREATE TABLE users(
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL, 
    admin BOOLEAN DEFAULT 0 NOT NULL
    )' || true
sqlite3 $DB '
    CREATE TABLE papers(
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    date TEXT NOT NULL,
    key_words TEXT
    )' || true
sqlite3 $DB '
    CREATE TABLE connections(
    citing TEXT NOT NULL REFERENCES papers(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    cited TEXT NOT NULL REFERENCES papers(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    value INT NOT NULL,
    PRIMARY KEY (citing, cited)
    )' || true
sqlite3 $DB '
    CREATE TABLE familiarities(
    user TEXT NOT NULL REFERENCES user(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    paper INT NOT NULL REFERENCES papers(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    value INT NOT NULL,
    PRIMARY KEY (user, paper)
    )' || true


#sqlite3 $DB < ./dummy_data/import.sql

