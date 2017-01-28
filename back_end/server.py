import flask
import httplib2
from oauth2client import client
import os
app = flask.Flask(__name__)

@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return 'Logged out <a href="' + flask.url_for('oauth2callback') + '">Log in</a>'
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return 'Logged out <a href="' + flask.url_for('oauth2callback') + '">Log in</a>'
  else:
    http_auth = credentials.authorize(httplib2.Http())
    return 'Logged in!'

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
    return flask.redirect(flask.url_for('index'))

if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()
