from flask import Flask, jsonify, render_template
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd

app = Flask(__name__)

client = Client(zwiftuser, zwiftpwd)
zwiftProfile = client.get_profile()


def get_activities_internal():
    return client.get_activity(zwiftProfile.profile["id"]).list()


def get_activityById_internal(activtiy_id):
    activity = None
    activities = get_activities_internal()
    for item in activities:
        if item["id"] == activtiy_id:
            activity = item
            break

    return activity


@app.route('/')
def index():
    items = ['Apfel', 'Banane', 'Orange', 'Mango', 'Traube']
    items = []
    activitis = get_activities_internal()

    for activity in activitis:
        items.append(activity["id"])

    return render_template('index.html', items=items)


@app.route('/activities', methods=['GET'])
def get_activities():
    activitiesList = get_activities_internal()
    return jsonify(activitiesList)


@app.route('/activities/<int:activtiy_id>', methods=['GET'])
def get_activityById(activtiy_id):
    activity = get_activityById_internal(activtiy_id)
    return jsonify(activity)


@app.route('/downloadlink/<int:activtiy_id>', methods=['GET'])
def get_linkById(activtiy_id):
    activity = get_activityById_internal(activtiy_id)
    link = "https://" + activity["fitFileBucket"] + \
        ".s3.amazonaws.com/" + activity["fitFileKey"]
    return link


""" 
@app.route('/activities/<int:profile_id>', methods=['GET'])
def get_activities(profile_id):
    activitiesList = client.get_activity(profile_id).list()
    return jsonify(activitiesList)

@app.route('/activities/<int:profile_id>/<int:activtiy_id>', methods=['GET'])
def get_activities(profile_id, activtiy_id):
    activitiesList = client.get_activity(profile_id).list()
    activity = activitiesList.get(activtiy_id)
    return jsonify(activity)
"""

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
