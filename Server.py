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
    return json.dumps({'report': grouplytics.overall_message_report()})


@app.route('/swear_word_report')
def swear_word_report():
    return json.dumps({'report': grouplytics.swear_word_report()})


@app.route('/donald_trump_report')
def donald_trump_report():
    return json.dumps('report': grouplytics.donald_trump_report()})


@app.route('/most_liked_report')
def most_liked_report():
    return json.dumps({'report': grouplytics.most_liked_report()})


@app.route('/biggest_liker_report')
def biggest_liker_report():
    return json.dumps({'report': grouplytics.biggest_liker_report()})


@app.route('/meme_lord_report')
def meme_lord_report():
    return json.dumps({'report': grouplytics.meme_lord_report()})


@app.route('/dude_report')
def dude_report():
    return json.dumps({'report': grouplytics.dude_report()})
