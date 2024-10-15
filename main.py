import asyncio
import json
import os.path
import sys

from datetime import datetime
from zwift import Client
from zrconfig import zwiftuser, zwiftpwd, runtoken

from methods import Portal, log, logError, uploadToRunalyze, convertDateTimeToUtcDate

from constants import FOLDER_DATA

def main():
    # Initialize Client
    client = Client(zwiftuser, zwiftpwd)
    zwiftProfile = client.get_profile()
    zwiftActivities = client.get_activity(zwiftProfile.profile["id"])
    activitiesList = zwiftActivities.list()

    # Import only after importdate
    if len(sys.argv) > 1:
        importdate = convertDateTimeToUtcDate(sys.argv[1]).Date()
    else:
        importdate = convertDateTimeToUtcDate(datetime.now()).Date()

    try:
        if not os.path.exists("data"):
            os.makedirs("data")

        with open("data/fitFiles.json", "w") as fitFilesFile:
            json.dump(activitiesList, fitFilesFile, indent=2)

        for activity in activitiesList:
            if convertDateTimeToUtcDate(activity["endDate"]) > importdate: # pd.to_datetime(activity["endDate"]).tz_convert(None) > importdate:
                log("Activity ended after set importdate. Skipping.")
                continue

            fitFileName = FOLDER_DATA + convertDateTimeToUtcDate(activity["endDate"]).strftime("%Y%m%d_%H%M%S") + ".fit"

            if os.path.isfile(fitFileName):
                log("Already downloaded. Skipping")
                continue

            log("Processing: " + activity["name"] + " - Date: " + convertDateTimeToUtcDate(activity["endDate"]).strftime("%Y-%m-%d") + " - " + str(activity["distanceInMeters"] / 1000) + "km")
            link = "https://" + activity["fitFileBucket"] + ".s3.amazonaws.com/" + activity["fitFileKey"]
            asyncio.run(uploadToRunalyze(link, Portal.Zwift, fitFileName, runtoken, None, None))
    except:
        type, value, traceback = sys.exc_info()
        logError(str(value))
        pass
    finally:
        fitFilesFile.close()

main()