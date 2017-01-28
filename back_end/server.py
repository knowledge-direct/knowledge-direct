import flask
import httplib2
from oauth2client import client
import os
import json
import sqlite3
import requests

app = flask.Flask(__name__, static_url_path='/static')

conn = sqlite3.connect('db/database.db')

# Method for checking if a user exists, if not then creating a new record
# followed by returning the user's ID
# TODO: move this into a database/user class
def create_or_update_user(google_id, google_token):
    # Get a new cursor, and select the first row from the query
    c = conn.cursor()
    t = (str(google_id),)
    c.execute('SELECT id FROM users WHERE id=?', t)
    row = c.fetchone()
    # Check if a row was returned
    if row == None:
        # Send a request to Google to get the user's name
        r = requests.get('https://www.googleapis.com/plus/v1/people/me?access_token=' + google_token)
        # Get the name from the response, ready to insert
        t = (r.json()['displayName'], str(google_id))
        # Insert into the DB
        c.execute('INSERT INTO users (name, id, admin) VALUES (?, ?, 0)', t)
        # Return the ID
        return google_id
    else:
        # Return the ID
        return row[0]


# Get the name of the user from the database, given their ID
# TODO: move this into a database/user class
def get_user_name(user_id):
    c = conn.cursor()
    t = (user_id,)
    c.execute('SELECT name FROM users WHERE id=?', t)
    row = c.fetchone()
    if row == None:
        # Not found, return the empty string
        return ''
    else:
        return row[0]

@app.route('/')
def index():
    return flask.render_template('main.html')


@app.route('/logged_in')
def is_logged_in():
    # Check if session does not contain a user ID - ask for login
    if 'user_id' not in flask.session:
        return flask.jsonify({'status': False, 'name': '', 'redirect_uri': flask.url_for('oauth2callback') })
    # Get credentials from session
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    # If access token is expired - ask for login
    if credentials.access_token_expired:
        return flask.jsonify({'status': False, 'name': '', 'redirect_uri': flask.url_for('oauth2callback') })
    else:
        # User is logged in
        http_auth = credentials.authorize(httplib2.Http())
        return flask.jsonify({'status': True, 'name': get_user_name(flask.session['user_id']), 'redirect_uri': flask.url_for('oauth2callback') })

@app.route('/logout')
def logout():
    flask.session = []
    return flask.redirect(flask.url_for('index'))

@app.route('/oauth2callback')
def oauth2callback():
    # Callback from Google
    flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='profile',
      redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        flask.session['user_id'] = create_or_update_user(json.loads(credentials.to_json())['id_token']['sub'], json.loads(credentials.to_json())['access_token'])
        return flask.redirect(flask.url_for('index'))

if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()
