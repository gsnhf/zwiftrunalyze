
import aiofiles as aiof
import aiohttp
import json
import logging
import sys
import pandas as pd

from enum import Enum

from constants import RUNALYZE_UPLOAD_LINK

logging.basicConfig(filename='data/Runalyze.log',filemode='a', encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout)) 

class Portal(Enum):
    Zwift = 1
    MyWhoosh = 2


def log(message):
    logger.info(message)

def logError(message):
    logger.error(message)

async def write_fitFile(fileName, response):
    logger.debug(str(response.text))
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

async def upload(session, fileName, runalyzeToken):
    try:
        log(runalyzeToken)
        async with session.post(RUNALYZE_UPLOAD_LINK, data={'file': open(fileName, "rb")}, headers={"token": runalyzeToken}) as responsePost:
            log("post finished: " + str(responsePost.text))
    except:
        type, value, traceback = sys.exc_info()
        logError("runalyze error: " + str(value))
        pass

async def uploadToRunalyze(link, portal, fileName, runalyzeToken, sessionKey, token):
    try:
      async with aiohttp.ClientSession() as session:
        if portal == Portal.MyWhoosh:
            cookies = {
                'mywhooshweb_session': sessionKey
            }
            headers = {
                'authority': 'event.mywhoosh.com',
                'accept': 'application/json',
                'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6',
                'authorization': 'Bearer ' + token,
                'referer': 'https://event.mywhoosh.com/user/profile',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
            }
            async with session.get(link, cookies=cookies, headers=headers) as response1:
                # print(response1.status_code)
                x = await response1.content.read()
                y = json.loads(x.decode("utf8"))
                link = y.get('data').get('data')

            headers.pop('authorization')

        elif portal == Portal.Zwift:
            cookies = {}
            headers = {}
            
        async with session.get(link, cookies=cookies, headers=headers) as response:
            await write_fitFile(fileName, response)
            if runalyzeToken:
                await upload(session, fileName, runalyzeToken)
                
    except:
        type, value, traceback = sys.exc_info()
        logError(str(value))
        pass

def convertDateTimeToUtcDate(datetime, local_timezone='Europe/Berlin'):
    try:
        local_time = pd.to_datetime(datetime).tz_localize(local_timezone)
        utc_time = local_time.tz_convert('UTC')    
        return utc_time 
    except:
        return datetime