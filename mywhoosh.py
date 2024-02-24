import logging
import asyncio
import sys
import json
import os.path
import requests
import pandas as pd

from datetime import datetime
from zrconfig import mywhooshuser, mywhooshpwd

def log(message):
    logging.info(message)

def logError(message):
    logging.error(message)

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
    content = str(response.content)
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

    # die Datei myWhooshFitFiles laden
    if os.path.isfile(fitFilesJsonPath):
        with open(fitFilesJsonPath) as f:
            fitFilesJson = json.load(f)
            print(fitFilesJson)

    # daten vom server holen
    files = GetFitFilesFromMyWhooshServer()
    # fehlende hinzufügen
    # mit dem letzten uploaddatum vergleichen
    # noch nicht geuploadete files downloaden
    # nicht hochgeladene files nach runalyze hochladen

    createTimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    abc = {'timestamp': createTimestamp, 'files': files}
    
    with open(fitFilesJsonPath, "w") as fitFilesFile:
        json.dump(abc, fitFilesFile, indent=2)

main()