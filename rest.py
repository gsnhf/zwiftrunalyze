from flask import Flask, jsonify
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runalyzeToken

app = Flask(__name__)

client = Client(zwiftuser, zwiftpwd)
zwiftProfile = client.get_profile()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/activities', methods=['GET'])
def get_activities():
    activitiesList = client.get_activity(zwiftProfile.profile["id"]).list()
    return jsonify(activitiesList)

@app.route('/activities/<int:profile_id>', methods=['GET'])
def get_activities(profile_id):
    activitiesList = client.get_activity(profile_id).list()
    return jsonify(activitiesList)

@app.route('/activities/<int:activtiy_id>', methods=['GET'])
def get_activities(activtiy_id):
    activitiesList = client.get_activity(zwiftProfile.profile["id"]).list()
    activity = activitiesList.get(activtiy_id)
    return jsonify(activity)

@app.route('/activities/<int:profile_id>/<int:activtiy_id>', methods=['GET'])
def get_activities(profile_id, activtiy_id):
    activitiesList = client.get_activity(profile_id).list()
    activity = activitiesList.get(activtiy_id)
    return jsonify(activity)

data = {
    1: {"name": "Item 1", "description": "This is item 1"},
    2: {"name": "Item 2", "description": "This is item 2"},
}

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = data.get(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
