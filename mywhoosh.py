import asyncio
import json
import os.path
import pandas as pd
import requests
import sys

from datetime import datetime
from zrconfig import mywhooshuser, mywhooshpwd, runalyzeToken

from methods import log, logError, uploadToRunalyze, Portal

def Login():
    cookies = {}

    headers = {
        'authority': 'event.mywhoosh.com',
        'accept': 'application/json',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://event.mywhoosh.com',
        'referer': 'https://event.mywhoosh.com/auth/login',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }

    json_data = {
        'remember': False,
        'password': mywhooshpwd,
        'email': mywhooshuser,
    }
    response = requests.post('https://event.mywhoosh.com/api/auth/login', cookies=cookies, headers=headers, json=json_data) 
    return response

def GetFitFilesFromMyWhooshServer(response):
    contentJson = response.json()

    data = contentJson.get('data')
    user = data.get('user')
    files = user.get('files')

    for fitFile in files:
        log(fitFile.get('date') + ' ' + fitFile.get('url'))
    
    return files


def main():
    fitFilesJsonPath = "data/myWhooshFitFiles.json"
    createTimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Import only after importdate
    if len(sys.argv) > 1:
        importdate = pd.to_datetime(sys.argv[1])
    else:
        datetime_str = pd.to_datetime(datetime.now()).strftime("%Y.%m.%d")
        importdate = datetime.strptime(datetime_str, '%Y.%m.%d')

    log("ImportDate: " + str(importdate))
    # load previously data
    if os.path.isfile(fitFilesJsonPath):
        with open(fitFilesJsonPath) as fitFilesJson:
            fitFilesJson = json.load(fitFilesJson)
    else:
        fitFilesJson = {'timestamp': createTimestamp, 'files': []}

    # get data from mywhoosh server eva 14 uhr, jane 9:10
    response = Login()
    cook = response.cookies.get_dict()
    sessionKey = cook['mywhooshweb_session']

    filesFromServer = GetFitFilesFromMyWhooshServer(response)

    # add missing items
    itemsToAdd = []
    for fileFromServer in filesFromServer:
        id = fileFromServer.get('id')
        found = False
        for fitFile in fitFilesJson.get('files'):
            if fitFile.get('id') == id:
                found = True
                break
        
        if not found:
            itemsToAdd.append(fileFromServer)

    for foundItem in itemsToAdd:
        fitFilesJson.get('files').append(foundItem)

    if len(itemsToAdd) > 0:
        fitFilesJson['timestamp'] = createTimestamp
        fitFilesJson.get('files').sort(key = lambda x:x['uploaded_at'])
        with open(fitFilesJsonPath, "w") as fitFilesFile:
            json.dump(fitFilesJson, fitFilesFile, indent=2)

    # mit dem letzten uploaddatum vergleichen
    # noch nicht geuploadete files downloaden
    # nicht hochgeladene files nach runalyze hochladen

    x = fitFilesJson.get('files')
    
    for ff in x:
        if pd.to_datetime(ff.get('uploaded_at')).tz_convert(None) >= importdate:
            searchId = ff.get('id')
            fitFileName = "data/" + "myWhoosh_" + searchId + ".fit"
            token = response.json().get('data').get('token')
            link = 'https://event.mywhoosh.com/api/auth/download/file/' + searchId
            asyncio.run(uploadToRunalyze(link, Portal.MyWhoosh, fitFileName, runalyzeToken, sessionKey, token))

main()