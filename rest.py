from flask import Flask, jsonify, render_template, request
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runalyzeToken

from constants import RUNALYZE_UPLOAD_LINK

from methods import log, fetch_file, logError, upload_file

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

    titleChecked = request.args.get('titleChecked', 'false').lower() == 'true'
    noteChecked = request.args.get('noteChecked', 'false').lower() == 'true'
    download_url = get_link_by_id(activity_id)
    activity = get_activity_by_id_internal(activity_id)

    file_content = await fetch_file(download_url)

    upload_params = {
        'url': RUNALYZE_UPLOAD_LINK,
        'file_content': file_content,
        'activity_id': activity_id,
        'runalyzeToken': runalyzeToken
    }

    if titleChecked and activity and 'name' in activity:
        upload_params['title'] = activity['name']
    if noteChecked and activity and 'description' in activity:
        upload_params['note'] = activity['note']

    upload_response = upload_file(**upload_params)

    txt = jsonify({
        "message": "File transferred successfully",
        "response": str(upload_response.text),
        "titleChecked": titleChecked,
        "noteChecked": noteChecked
    })
    log(f"transfer_file route completed for activity_id: {activity_id} with status code: {upload_response.status_code}")
    return txt, upload_response.status_code



@app.route('/log', methods=['POST'])
def log_message():
    data = request.get_json()
    message = data.get('message')
    if message:
        log(message)
        return jsonify({"status": "success", "message": "Log entry created"}), 200
    else:
        return jsonify({"status": "error", "message": "No log message provided"}), 400


@app.route('/logError', methods=['POST'])
def log_error():
    data = request.get_json()
    message = data.get('message')
    if message:
        logError(message)
        return jsonify({"status": "success", "message": "Log entry created"}), 200
    #else:
        #return jsonify({"status": "error", "message": "No log message provided"}), 400

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "success", "message": "Server is running"}), 200


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
