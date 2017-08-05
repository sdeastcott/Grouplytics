from flask import Flask, request, jsonify, session, render_template
from src.grouplytics import Grouplytics
from src.group import Group
app = Flask(__name__)

SECRET_KEY = "development key"
app.config.from_object(__name__)
app.config.from_envvar("APPLICATION_CONFIG", silent=True)

@app.route('/')
def home():
    return render_template('login.html')

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


if __name__ == "__main__":
    app.run()
