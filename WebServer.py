from flask import Flask
from src.Grouplytics import Grouplytics
from src.GroupMeWrapper import GroupMeWrapper
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
