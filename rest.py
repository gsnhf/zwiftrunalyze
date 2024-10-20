from flask import Flask, jsonify, render_template
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runalyzeToken
from flask_cors import CORS
import io

from constants import RUNALYZE_UPLOAD_LINK

import requests
import aiohttp

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
    
async def read_bytes_from_stream(stream_reader, num_bytes):
    data = await stream_reader.read(num_bytes)
    return data

async def fetch_file(url):
    async with aiohttp.ClientSession() as session:
        cookies = {}
        headers = {}
        async with session.get(url, cookies=cookies, headers=headers) as response:
            return await response.content.read()

def upload_file(url, file_content,activtiy_id):
    activityFileName=str(activtiy_id)+'.fit'
    file_like_object = io.BytesIO(file_content)
    buffered_reader = io.BufferedReader(file_like_object)

    files = {'file': (activityFileName, buffered_reader, 'application/octet-stream')}
    headers = {'token': runalyzeToken}
    response = requests.post(RUNALYZE_UPLOAD_LINK, headers=headers, files=files)
    return response
    
@app.route('/transferfile/<int:activtiy_id>', methods=['GET'])
async def transfer_file(activtiy_id):
    download_url = get_linkById(activtiy_id)

    file_content = await fetch_file(download_url)
    upload_response = upload_file(RUNALYZE_UPLOAD_LINK, file_content,activtiy_id)

    txt = jsonify({"message": "File transferred successfully: " + str( upload_response.text )})
    print(txt)
    return txt, upload_response.status_code


if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True)
# asyncio.run(main())