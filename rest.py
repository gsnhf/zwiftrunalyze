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
    activities = get_activities_internal()
    items = [activity for activity in activities]
    return render_template('index.html', items=items)


@app.route('/activities', methods=['GET'])
def get_activities():
    activities_list = get_activities_internal()
    return jsonify(activities_list)


@app.route('/activities/<int:activity_id>', methods=['GET'])
def get_activity_by_id(activity_id):
    activity = get_activity_by_id_internal(activity_id)
    return jsonify(activity)


@app.route('/downloadlink/<int:activity_id>', methods=['GET'])
def get_link_by_id(activity_id):
    activity = get_activity_by_id_internal(activity_id)
    link = f"https://{activity['fitFileBucket']}.s3.amazonaws.com/{activity['fitFileKey']}"
    return link


async def read_bytes_from_stream(stream_reader, num_bytes):
    data = await stream_reader.read(num_bytes)
    return data


async def fetch_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.content.read()


def upload_file(url, file_content, activity_id):
    activity_file_name = f"{activity_id}.fit"
    file_like_object = io.BytesIO(file_content)
    buffered_reader = io.BufferedReader(file_like_object)

    files = {'file': (activity_file_name, buffered_reader, 'application/octet-stream')}
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
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
