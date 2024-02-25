import json
import logging
import os.path
import requests

from datetime import datetime
from zrconfig import mywhooshuser, mywhooshpwd

from methods import log, logError, uploadToRunalyze

def GetFitFilesFromMyWhooshServer():
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
    contentJson = response.json()

    data = contentJson.get('data')
    user = data.get('user')
    files = user.get('files')

    for fitFile in files:
        log(fitFile.get('date') + ' ' + fitFile.get('url'))
    
    return files


def main():
    logging.basicConfig(filename='data/MywhooshRunalyze.log', encoding='utf-8', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))   

    fitFilesJsonPath = "data/myWhooshFitFiles.json"

    # load previously data
    if os.path.isfile(fitFilesJsonPath):
        with open(fitFilesJsonPath) as fitFilesJson:
            fitFilesJson = json.load(fitFilesJson)

    # get data from mywhoosh server
    filesFromServer = GetFitFilesFromMyWhooshServer()

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
        with open(fitFilesJsonPath, "w") as fitFilesFile:
            json.dump(fitFilesJson, fitFilesFile, indent=2)

    # mit dem letzten uploaddatum vergleichen
    # noch nicht geuploadete files downloaden
    # nicht hochgeladene files nach runalyze hochladen

    createTimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    abc = {'timestamp': createTimestamp, 'files': filesFromServer}
    
    with open(fitFilesJsonPath, "w") as fitFilesFile:
        json.dump(abc, fitFilesFile, indent=2)

main()