from flask import Flask, request, jsonify, session, render_template
from src.grouplytics import Grouplytics
from src.groupme import GroupMe
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


@app.route('/groups', methods=['GET'])
def groups():
    token = session.get('token', None)
    if token is None: return 'Error'





@app.route('/reports', methods=['POST'])
def reports():
    token = session.get('token', None)
    if token is None: return 'Error'
    
    query = request.get_json()
    groupme = GroupMe(token)
    members = groupme.get_members(query['group_id'])
    messages = groupme.get_messages(query['group_id'], members)
    grouplytics = Grouplytics(groupme.messages, groupme.members)

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
