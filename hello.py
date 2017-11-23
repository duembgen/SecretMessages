from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, flash, url_for, g, redirect
import atexit
import cf_deployment_tracker
import os
import sys
import json

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)
app.config.from_object('config')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

def decode_message(message, key):
    return 'decoded "{}" with key {}'.format(message, key)
	
def encode_message(message, key):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    newMessage = ''
    key = int(key)
    for character in message:
        if character in alphabet:
            position = alphabet.find(character)
            newPosition = (position + key) % 26
            newCharacter = alphabet[newPosition]
            newMessage += newCharacter
        else:
            newMessage += character
    return 'encoded "{}" with key {}'.format(newMessage, key)


@app.route('/')
@app.route('/index/')
def index():	
    print('showing index...', file=sys.stderr)
    return render_template('index.html', title='Home')
	
@app.route('/encode/', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        print('got POST', request.form, file=sys.stderr)
        key = request.form.get('key', None)

        flash('encode')
        decoded = request.form.get('message', None)
        encoded = encode_message(decoded, key)
        return render_template('messages.html', result=encoded, message='', key=key, action="Write")

    return render_template("messages.html", key=1, action="Write")

@app.route('/decode/', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        print('got POST', request.form, file=sys.stderr)
        key = request.form.get('key', None)
        
        flash('decode')
        encoded = request.form.get('message', None)
        decoded = decode_message(encoded, key)
        return render_template('messages.html', message=encoded, result=decoded, key=key, action="Read")

    return render_template("messages.html", key=1, action="Read")

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
