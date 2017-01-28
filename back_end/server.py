import flask
import httplib2
from oauth2client import client
import os
import json
import sqlite3
import requests

app = flask.Flask(__name__)

conn = sqlite3.connect('db/database.db')

def create_or_update_user(google_id, google_token):
    # Do this instead
    c = conn.cursor()
    print(google_token)
    t = (str(google_id),)
    c.execute('SELECT id FROM users WHERE id=?', t)
    row = c.fetchone()
    if row == None:
        headers = {'access_token': str(google_token)}
        r = requests.get('https://www.googleapis.com/plus/v1/people/me?access_token=' + google_token, headers=headers)
        t = (r.json()['displayName'], str(google_id))
        c.execute('INSERT INTO users (name, id, admin) VALUES (?, ?, 0)', t)
        t = (str(google_id),)
        c.execute('SELECT id FROM users WHERE id=?', t)
        return c.fetchone()[0]
    else:
        return row[0]


def get_user_name(user_id):
    c = conn.cursor()
    t = (user_id,)
    c.execute('SELECT name FROM users WHERE id=?', t)
    row = c.fetchone()
    if row == None:
        return ''
    else:
        return row[0]


@app.route('/')
def index():
  if 'user_id' not in flask.session:
    return 'Logged out <a href="' + flask.url_for('oauth2callback') + '">Log in</a>'
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return 'Logged out <a href="' + flask.url_for('oauth2callback') + '">Log in</a>'
  else:
    http_auth = credentials.authorize(httplib2.Http())
    return 'Logged in as ' + get_user_name(flask.session['user_id']) + '!'

@app.route('/oauth2callback')
def oauth2callback():
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
