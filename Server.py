import json
from flask import Flask
from src.Grouplytics import Grouplytics
from src.GroupMeWrapper import GroupMeWrapper
app = Flask(__name__)

@app.route('/initialize/<token>/<name>/<members>')
def init():
    global groupme
    global grouplytics

    groupme = GroupMeWrapper(token, name, members)
    grouplytics = Grouplytics(groupme.members, groupme.messages)


@app.route('/overall_message_report')
def overall_message_report():
    return json.dumps({'title': 'Overall Message Report', 'report': grouplytics.overall_message_report()})


@app.route('/swear_word_report')
def swear_word_report():
    return json.dumps({'title': 'Swear Word Report', 'report': grouplytics.swear_word_report()})


@app.route('/avg_word_length')
def avg_word_length():
    return json.dumps({'title': 'Average Word Length', 'report': grouplytics.avg_word_length()})


@app.route('/likes_received')
def likes_received():
    return json.dumps({'title': 'Likes Received', 'report': grouplytics.likes_received()})


@app.route('/messages_liked')
def messages_liked():
    return json.dumps({'title': 'Messages Liked', 'report': grouplytics.messages_liked()})


@app.route('/images_shared')
def meme_lord_report():
    return json.dumps({'title': 'Images Shared', 'report': grouplytics.images_shared()})


@app.route('/dude_report')
def dude_report():
    return json.dumps({'title': 'Dude Report', 'report': grouplytics.dude_report()})
