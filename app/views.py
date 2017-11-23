import os, sys
from flask import flash, render_template, request, redirect, url_for, g
from app import app 

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
