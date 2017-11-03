import os
basedir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secretmessages'
UPLOAD_FOLDER = 'static/'