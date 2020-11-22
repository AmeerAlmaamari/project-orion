import os
from flask import Flask

UPLOAD_FOLDER = 'projectOrion/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from projectOrion import routes