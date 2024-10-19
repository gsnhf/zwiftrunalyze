from flask import Flask, jsonify, request, render_template
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runalyzeToken
from flask_cors import CORS

from constants import RUNALYZE_UPLOAD_LINK

import requests

app = Flask(__name__)
CORS(app)

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
    activitis = get_activities_internal()
    items = []

    for activity in activitis:
        items.append(activity)

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
    
@app.route('/transferfile/<int:activtiy_id>', methods=['GET'])
def transfer_file(activtiy_id):
    # URL der Datei, die heruntergeladen werden soll
    download_url = get_linkById(activtiy_id)
    # URL des Services, zu dem die Datei hochgeladen werden soll
    upload_url = RUNALYZE_UPLOAD_LINK # request.json.get('upload_url')

    # Datei herunterladen
    response = requests.get(download_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to download file"}), 400

    # Datei hochladen
    files = {"file": (str(activtiy_id)+".fit",response.content)}

    headers = {"token": runalyzeToken}
    # headers = {'Authorization': f'Bearer {runalyzeToken}'}

    upload_response = requests.post(upload_url, files=files, headers=headers)
    if upload_response.status_code  >= 400:
        return jsonify({"error": "Failed to upload file"}), upload_response.status_code

    return jsonify({"message": "File transferred successfully"}), upload_response.status_code


if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True)
