import aiohttp
import asyncio
import aiofiles as aiof
import logging
import sys
import json
import os.path
import pandas as pd

from datetime import datetime
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runtoken

def log(message):
    logging.info(message)

def logError(message):
    logging.error(message)

async def download_file(activity, fileName, runtoken):
    try:
      log("Processing: " + activity["name"] + " - Date: " + pd.to_datetime(activity["endDate"]).strftime("%Y-%m-%d") + " - " + str(activity["distanceInMeters"] / 1000) + "km")
      link = "https://" + activity["fitFileBucket"] + ".s3.amazonaws.com/" + activity["fitFileKey"]

      async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            logging.debug(str(response.text))
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
            if runtoken:
                try:
                    async with session.post("https://runalyze.com/api/v1/activities/uploads", data={'file': open(fileName, "rb")}, headers={"token": runtoken}) as responsePost:
                        log("post finished: " + str(responsePost.text))
                except:
                    type, value, traceback = sys.exc_info()
                    logError("runalyze error: " + str(value))
                    pass
    except:
        type, value, traceback = sys.exc_info()
        logError(str(value))
        pass

def main():
    logging.basicConfig(filename='data/zwiftrunalyze.log', encoding='utf-8', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # Initialize Client
    client = Client(zwiftuser, zwiftpwd)
    zwiftProfile = client.get_profile()
    zwiftActivities = client.get_activity(zwiftProfile.profile["id"])
    activitiesList = zwiftActivities.list()

    # Import only after importdate
    if len(sys.argv) > 1:
        importdate = pd.to_datetime(sys.argv[1])
    else:
        importdate = pd.to_datetime(datetime.now())

    try:
        if not os.path.exists("data"):
            os.makedirs("data")

        with open("data/fitFiles.json", "w") as fitFilesFile:
            json.dump(activitiesList, fitFilesFile, indent=2)

        for activity in activitiesList:
            if pd.to_datetime(activity["endDate"]).tz_convert(None) > importdate:
                log("Activity ended after set importdate. Skipping.")
                continue

            fitFileName = "data/" + pd.to_datetime(activity["endDate"]).strftime("%Y%m%d_%H%M%S") + ".fit"

            if os.path.isfile(fitFileName):
                log("Already downloaded. Skipping")
                continue

            asyncio.run(download_file(activity, fitFileName, runtoken))
    except:
        type, value, traceback = sys.exc_info()
        logError(str(value))
        pass
    finally:
        fitFilesFile.close()

main()