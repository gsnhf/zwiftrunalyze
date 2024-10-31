import aiofiles as aiof
import aiohttp
import json
import logging
import logging.handlers
import os
import sys
import pandas as pd
import io
import requests

from enum import Enum
from constants import RUNALYZE_UPLOAD_LINK

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler = logging.handlers.TimedRotatingFileHandler('logs/app.log', when='midnight', interval=1, backupCount=5)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)

logger = logging.getLogger('app_logger')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(logging.StreamHandler(sys.stdout))

class Portal(Enum):
    Zwift = 1
    MyWhoosh = 2

def log(message):
    logger.info(message)

def logError(message):
    logger.error(message)

async def write_fitFile(fileName, response):
    log(f"write_fitFile started for fileName: {fileName}")
    async with aiof.open(fileName, "wb") as fitFile:
        empty_bytes = b''
        result = empty_bytes
        while True:
            chunk = await response.content.read(8)
            if chunk == empty_bytes:
                break
            result += chunk 
        await fitFile.write(result)
        await fitFile.flush()
    log(f"write_fitFile completed for fileName: {fileName}")

async def upload(session, fileName, runalyzeToken):
    log(f"upload started for fileName: {fileName}")
    try:
        async with session.post(RUNALYZE_UPLOAD_LINK, data={'file': open(fileName, "rb")}, headers={"token": runalyzeToken}) as responsePost:
            log("post finished: " + await responsePost.text())
    except Exception as e:
        logError(f"runalyze error: {e}")
    log(f"upload completed for fileName: {fileName}")

async def uploadToRunalyze(link, portal, fileName, runalyzeToken, sessionKey, token):
    log(f"uploadToRunalyze started for fileName: {fileName}")
    try:
        async with aiohttp.ClientSession() as session:
            if portal == Portal.MyWhoosh:
                cookies = {'mywhooshweb_session': sessionKey}
                headers = {
                    'authority': 'event.mywhoosh.com',
                    'accept': 'application/json',
                    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6',
                    'authorization': f'Bearer {token}',
                    'referer': 'https://event.mywhoosh.com/user/profile',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                }
                async with session.get(link, cookies=cookies, headers=headers) as response1:
                    response_data = await response1.content.read()
                    json_data = json.loads(response_data.decode("utf8"))
                    link = json_data.get('data').get('data')
                headers.pop('authorization')

            async with session.get(link, cookies=cookies, headers=headers) as response:
                await write_fitFile(fileName, response)
                if runalyzeToken:
                    await upload(session, fileName, runalyzeToken)
    except Exception as e:
        logError(f"Error in uploadToRunalyze: {e}")
    log(f"uploadToRunalyze completed for fileName: {fileName}")

def convertDateTimeToUtcDate(datetime, local_timezone='Europe/Berlin'):
    log(f"convertDateTimeToUtcDate started for datetime: {datetime}")
    try:
        local_time = pd.to_datetime(datetime).tz_localize(local_timezone)
        utc_time = local_time.tz_convert('UTC')    
        log(f"convertDateTimeToUtcDate completed for datetime: {datetime}")
        return utc_time 
    except Exception as e:
        logError(f"Error in convertDateTimeToUtcDate: {e}")
        return datetime


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

def upload_file(url, file_content, activity_id, runalyzeToken, title=None, note=None):
    log(f"upload_file started for activity_id: {activity_id}")
    activity_file_name = f"{activity_id}.fit"
    file_like_object = io.BytesIO(file_content)
    buffered_reader = io.BufferedReader(file_like_object)

    files = {'file': (activity_file_name, buffered_reader, 'application/octet-stream')}
    headers = {'token': runalyzeToken}
    data = {}
    if title:
        data['title'] = title
    if note:
        data['note'] = note
    response = requests.post(url, headers=headers, files=files, data=data)
    log(f"upload_file completed for activity_id: {activity_id} with status code: {response.status_code}")
    return response