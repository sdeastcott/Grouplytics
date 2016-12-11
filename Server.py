import json
from flask import Flask, request
from src.Grouplytics import Grouplytics
from src.GroupMeWrapper import GroupMeWrapper
app = Flask(__name__)


@app.route('/overall_message_report', methods=["POST"])
def overall_message_report():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return json.dumps({'title': 'Overall Message Report', 'report': grouplytics.overall_message_report()})


@app.route('/swear_word_report')
def swear_word_report():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return json.dumps({'title': 'Swear Word Report', 'report': grouplytics.swear_word_report()})


@app.route('/avg_word_length')
def avg_word_length():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return json.dumps({'title': 'Average Word Length', 'report': grouplytics.avg_word_length()})


@app.route('/likes_received')
def likes_received():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return json.dumps({'title': 'Likes Received', 'report': grouplytics.likes_received()})


@app.route('/messages_liked')
def messages_liked():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return json.dumps({'title': 'Messages Liked', 'report': grouplytics.messages_liked()})


@app.route('/images_shared')
def meme_lord_report():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return json.dumps({'title': 'Images Shared', 'report': grouplytics.images_shared()})


@app.route('/dude_report')
def dude_report():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return json.dumps({'title': 'Dude Report', 'report': grouplytics.dude_report()})


if __name__ == "__main__":
    app.run()
