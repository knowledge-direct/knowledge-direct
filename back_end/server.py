import flask
import httplib2
from oauth2client import client
import os
import json
import sqlite3
from db import database

app = flask.Flask(__name__, static_url_path='/static')

d = database.Database('db/database.db')


def user_logged_in(session):
    user_name = None
    if 'user_id' in flask.session:
        user_name = d.get_user_name(flask.session['user_id'])
    if user_name == '' or user_name == None:
        return False
    return True


@app.route('/')
def index():
    user_name = None
    if 'user_id' in flask.session:
        user_name = d.get_user_name(flask.session['user_id'])
    if user_name == '':
        user_name = None
    if user_logged_in(flask.session):
        unread_papers = d.list_papers_unread(flask.session['user_id'])
        read_papers = d.list_papers_read(flask.session['user_id'])
        return flask.render_template('logged_in.html', user_name=user_name, unread_papers=unread_papers, read_papers=read_papers)
    else:
        return flask.render_template('main.html', user_name=user_name)

@app.route('/search', methods=['GET'])
def search():
    target = None
    start_papers = []
    for item in flask.request.form.items():
        if item[0] == 'target':
            target = item[1]
        else:
            if item[1] == 'on':
                start_papers += [item[0]]
    search_data = { 'target': target, 'start_papers': start_papers }
    return flask.jsonify(search_data)

@app.route('/mark_read', methods=['POST'])
def mark_read():
    if user_logged_in(flask.session):
        d.add_familiar(flask.session['user_id'], flask.request.form['paper'])
    return flask.jsonify({})


@app.route('/mark_unread', methods=['POST'])
def mark_unread():
    if user_logged_in(flask.session):
        d.remove_familiar(flask.session['user_id'], flask.request.form['paper'])
    return flask.jsonify({})


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
        return flask.jsonify({'status': True, 'name': d.get_user_name(flask.session['user_id']), 'redirect_uri': flask.url_for('oauth2callback') })

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
        flask.session['user_id'] = d.create_or_update_user(json.loads(credentials.to_json())['id_token']['sub'], json.loads(credentials.to_json())['access_token'])
        return flask.redirect(flask.url_for('index'))

if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()
