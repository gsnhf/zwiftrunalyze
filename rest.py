from flask import Flask, jsonify, render_template
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runalyzeToken

from constants import RUNALYZE_UPLOAD_LINK

from methods import log, fetch_file, upload_file

app = Flask(__name__)

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


@app.route('/transferfile/<int:activity_id>', methods=['GET'])
async def transfer_file(activity_id):
    log(f"transfer_file route started for activity_id: {activity_id}")
    download_url = get_link_by_id(activity_id)

    file_content = await fetch_file(download_url)
    upload_response = upload_file(RUNALYZE_UPLOAD_LINK, file_content, activity_id, runalyzeToken)

    txt = jsonify({"message": "File transferred successfully: " + str(upload_response.text)})
    log(f"transfer_file route completed for activity_id: {activity_id} with status code: {upload_response.status_code}")
    return txt, upload_response.status_code


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5005'
    response.headers['Access-Control-Allow-Methods'] = 'GET'#'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
