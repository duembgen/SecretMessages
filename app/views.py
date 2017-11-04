import os, sys
import time
from flask import flash, render_template, request, redirect, url_for, g
from werkzeug.utils import secure_filename
from app import app 

def decode_message(message, key):
    return 'decoded {}'.format(message)
	
def encode_message(message, key):
    return 'encoded {}'.format(message)


@app.route('/')
@app.route('/index/')
def index():	
    print('showing index...', file=sys.stderr)
    return render_template('index.html', title='Home')
	
@app.route('/messages/', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        print('got POST', request.form, file=sys.stderr)
        key = request.form.get('key', None)
        
        if "decode" in request.form.values():
            flash('decode')
            encoded = request.form.get('encoded', None)
            decoded = decode_message(encoded, key)
            return render_template('messages.html', decoded=decoded, encoded=encoded)

        elif "encode" in request.form.values():
            flash('encode')
            decoded = request.form.get('decoded', None)
            encoded = encode_message(decoded, key)
            return render_template('messages.html', encoded=encoded, decoded='')

    return render_template("messages.html")