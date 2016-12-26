from flask import Flask, request, jsonify, session
from src.grouplytics import Grouplytics
from src.groupme_wrapper import GroupMeWrapper
app = Flask(__name__)

SECRET_KEY = "development key"
app.config.from_object(__name__)
app.config.from_envvar("APPLICATION_CONFIG", silent=True)


@app.route('/callback')
def receive_token():
    token = request.args.get('access_token', None)
    if token is None:
        return 'Error'  # Return an unauthorized code
    else:
        session['token'] = token
        return 'Success'  # Redirect to a route handled by the web app

@app.route('/all_reports', methods=['POST'])
def all_reports():
    token = session.get('token', None)
    if token is None:
        return 'Error'
    else:
        query = request.get_json()
        groupme = GroupMeWrapper(token, query['name'], query['members'])
        grouplytics = Grouplytics(groupme.members, groupme.messages)
        return jsonify([
            grouplytics.overall_message_report(),
            grouplytics.likes_received(),
            grouplytics.likes_received_per_message(),
            grouplytics.messages_liked(),
            grouplytics.average_word_length(),
            grouplytics.swear_word_report(),
            grouplytics.dude_report(),
            grouplytics.images_shared()
        ])

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
