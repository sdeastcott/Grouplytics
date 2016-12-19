from flask import Flask, request, jsonify
from src.Grouplytics import Grouplytics
from src.GroupMeWrapper import GroupMeWrapper
app = Flask(__name__)


'''*******************
Right now we're making calls to the GroupMe API for every single report. This is 
obviously terribly inefficient. A future change will be made once we figure out
how we're handling data storage.
********************'''

@app.route('/overall_message_report', methods=["POST"])
def overall_message_report():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return jsonify({'title': 'Overall Message Report',
                    'report': grouplytics.overall_message_report()})


@app.route('/swear_word_report', methods=["POST"])
def swear_word_report():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return jsonify({'title': 'Swear Word Report',
                    'report': grouplytics.swear_word_report()})


@app.route('/avg_word_length', methods=["POST"])
def avg_word_length():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return jsonify({'title': 'Average Word Length',
                    'report': grouplytics.avg_word_length()})


@app.route('/likes_received', methods=["POST"])
def likes_received():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return jsonify({'title': 'Likes Received',
                    'report': grouplytics.likes_received()})


@app.route('/messages_liked', methods=["POST"])
def messages_liked():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return jsonify({'title': 'Messages Liked',
                      'report': grouplytics.messages_liked()})


@app.route('/images_shared', methods=["POST"])
def meme_lord_report():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return jsonify({'title': 'Images Shared',
                      'report': grouplytics.images_shared()})


@app.route('/dude_report', methods=["POST"])
def dude_report():
    data = request.get_json()
    groupme = GroupMeWrapper(data['token'], data['name'], data['members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)
    return jsonify(**{'title': 'Dude Report', 'report': grouplytics.dude_report()})


if __name__ == "__main__":
    app.run()
