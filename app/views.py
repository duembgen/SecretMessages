import os, sys
import time
from flask import render_template, request, redirect, url_for, g
from werkzeug.utils import secure_filename
from app import app #, models #, db
#from models import Page

@app.route('/')
@app.route('/index')
def index():	
    print('showing index...')
    return render_template('index.html', title='Home')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/keyword_mapping')
@app.route('/keyword_mapping', methods=['GET','POST'])
def keyword_entry():
    return render_template('keyword_mapping.html', pages=pages)
