from flask import Flask, jsonify, request, render_template
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runalyzeToken
from flask_cors import CORS
import sys

from constants import RUNALYZE_UPLOAD_LINK

import requests

import aiofiles as aiof
import aiohttp
import asyncio

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
            #a= await response.read()
            #return a
            return  response.content.read()

async def upload_file(url, file_content,activtiy_id):
    async with aiohttp.ClientSession() as session:
        data1 = aiohttp.FormData()
        fname=str(activtiy_id)+'.fit'
        data1.add_field('file', file_content, filename=fname, content_type='multipart/form-data')
        
        async with session.post(url, data={'file': data1}, headers={"token": runalyzeToken}) as response:
            txt = await response.text()
            print(txt)
            return response
    
@app.route('/transferfile/<int:activtiy_id>', methods=['GET'])
async def transfer_file(activtiy_id):
    download_url = get_linkById(activtiy_id)

    file_content = await fetch_file(download_url)
    upload_response = await upload_file(RUNALYZE_UPLOAD_LINK, file_content,activtiy_id)

    txt1 = str(await upload_response.text())
    txt = jsonify({"message": "File transferred successfully: " + txt1})
    txt2 = await upload_response.text()
    print(txt1)
    print(txt2)
    return txt, upload_response.status

    async with aiohttp.ClientSession() as session:
        cookies = {}
        headers = {}
        async with session.get(download_url, cookies=cookies, headers=headers) as response:
            try:
                # await response.content.drain()
                data = await read_bytes_from_stream(response.content, 1024)
                async with session.post(RUNALYZE_UPLOAD_LINK, data={'file': (str(activtiy_id)+".fit",data)}, headers={"token": runalyzeToken}) as responsePost:
                    return jsonify({"message": "File transferred successfully: " + str(responsePost.text)}), responsePost.status
            except:
                type, value, traceback = sys.exc_info()
                return jsonify({"error": "Failed to upload file: " + str(value)}), responsePost.status


if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True)
# asyncio.run(main())