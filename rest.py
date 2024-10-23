from flask import Flask, jsonify, render_template
import aiohttp
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runalyzeToken
from flask_cors import CORS
import io

from constants import RUNALYZE_UPLOAD_LINK

import requests
from methods import log, logError, uploadToRunalyze, convertDateTimeToUtcDate

app = Flask(__name__)
CORS(app)

client = Client(zwiftuser, zwiftpwd)
zwiftProfile = client.get_profile()


def get_activities_internal():
    log("get_activities_internal started")
    activities = client.get_activity(zwiftProfile.profile["id"]).list()
    log("get_activities_internal completed")
    return activities


def get_activity_by_id_internal(activity_id):
    log(f"get_activity_by_id_internal started for activity_id: {activity_id}")
    activity = None
    activities = get_activities_internal()
    for item in activities:
        if item["id"] == activity_id:
            activity = item
            break
    log(f"get_activity_by_id_internal completed for activity_id: {activity_id}")
    return activity


@app.route('/')
def index():
    log("index route started")
    activities = get_activities_internal()
    items = [activity for activity in activities]
    log("index route completed")
    return render_template('index.html', items=items)


@app.route('/activities', methods=['GET'])
def get_activities():
    log("get_activities route started")
    activities_list = get_activities_internal()
    log("get_activities route completed")
    return jsonify(activities_list)


@app.route('/activities/<int:activity_id>', methods=['GET'])
def get_activity_by_id(activity_id):
    log(f"get_activity_by_id route started for activity_id: {activity_id}")
    activity = get_activity_by_id_internal(activity_id)
    log(f"get_activity_by_id route completed for activity_id: {activity_id}")
    return jsonify(activity)


@app.route('/downloadlink/<int:activity_id>', methods=['GET'])
def get_link_by_id(activity_id):
    log(f"get_link_by_id route started for activity_id: {activity_id}")
    activity = get_activity_by_id_internal(activity_id)
    link = f"https://{activity['fitFileBucket']}.s3.amazonaws.com/{activity['fitFileKey']}"
    log(f"get_link_by_id route completed for activity_id: {activity_id}")
    return link


async def read_bytes_from_stream(stream_reader, num_bytes):
    log("read_bytes_from_stream started")
    data = await stream_reader.read(num_bytes)
    log("read_bytes_from_stream completed")
    return data


async def fetch_file(url):
    log(f"fetch_file started for url: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.content.read()
            log(f"fetch_file completed for url: {url}")
            return data


def upload_file(url, file_content, activity_id):
    log(f"upload_file started for activity_id: {activity_id}")
    activity_file_name = f"{activity_id}.fit"
    file_like_object = io.BytesIO(file_content)
    buffered_reader = io.BufferedReader(file_like_object)

    files = {'file': (activity_file_name, buffered_reader, 'application/octet-stream')}
    headers = {'token': runalyzeToken}
    response = requests.post(RUNALYZE_UPLOAD_LINK, headers=headers, files=files)
    log(f"upload_file completed for activity_id: {activity_id} with status code: {response.status_code}")
    return response


@app.route('/transferfile/<int:activity_id>', methods=['GET'])
async def transfer_file(activity_id):
    log(f"transfer_file route started for activity_id: {activity_id}")
    download_url = get_link_by_id(activity_id)

    file_content = await fetch_file(download_url)
    upload_response = upload_file(RUNALYZE_UPLOAD_LINK, file_content, activity_id)

    txt = jsonify({"message": "File transferred successfully: " + str(upload_response.text)})
    log(f"transfer_file route completed for activity_id: {activity_id} with status code: {upload_response.status_code}")
    return txt, upload_response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
