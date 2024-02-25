import asyncio
import json
import logging
import os.path
import pandas as pd
import sys

from datetime import datetime
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runtoken

from methods import log, logError, uploadToRunalyze

def main():
    logging.basicConfig(filename='data/ZwiftRunalyze.log', encoding='utf-8', level=logging.INFO)
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

            log("Processing: " + activity["name"] + " - Date: " + pd.to_datetime(activity["endDate"]).strftime("%Y-%m-%d") + " - " + str(activity["distanceInMeters"] / 1000) + "km")
            link = "https://" + activity["fitFileBucket"] + ".s3.amazonaws.com/" + activity["fitFileKey"]
            asyncio.run(uploadToRunalyze(link, fitFileName, runtoken))
    except:
        type, value, traceback = sys.exc_info()
        logError(str(value))
        pass
    finally:
        fitFilesFile.close()

main()