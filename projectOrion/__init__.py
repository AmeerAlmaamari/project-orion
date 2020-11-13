import os
from flask import Flask
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'projectOrion/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['SECRET_KEY'] = '65a654d4231b321e321f32a1987c96'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from projectOrion import routes