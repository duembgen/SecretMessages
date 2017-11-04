import os, sys
import time
from flask import render_template, request, redirect, url_for, g
from werkzeug.utils import secure_filename
from app import app 

@app.route('/')
@app.route('/index')
def index():	
    print('showing index...')
    return render_template('index.html', title='Home')

@app.route('/messages', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        text = request.files['file']
        print('recorded:',text)
        return redirect(url_for('index'))
    return render_template('messages.html')