import sys
import json
import os.path
import requests
import pandas as pd

from datetime import datetime
from zwift import Client  # pip install zwift-client
from zrconfig import zwiftuser, zwiftpwd, runtoken

def printText(text):
    print(str(datetime.now()) + ": "+ text)

def main():
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
                printText("Activity ended after set importdate. Skipping.")
                continue
            link = "https://" + activity["fitFileBucket"] + ".s3.amazonaws.com/" + activity["fitFileKey"]

            fNameShort = pd.to_datetime(activity["endDate"]).strftime("%Y%m%d_%H%M%S")

            fName = "data/" + fNameShort

            fitFileName = fName + ".fit"

            if os.path.isfile(fitFileName):
                printText("Already downloaded. Skipping")
                continue

            printText("Processing: " + activity["name"] + " - Date: " + pd.to_datetime(activity["endDate"]).strftime("%Y-%m-%d") + " - " + str(activity["distanceInMeters"] / 1000) + "km")

            res = requests.get(link)
            with open(fitFileName, "wb") as fitFile:
                fitFile.write(res.content)
            if runtoken:
                runalyzePostResponse = requests.post("https://runalyze.com/api/v1/activities/uploads", files={'file': open(fitFileName, "rb")}, headers={"token": runtoken})
                printText(runalyzePostResponse.text)
    except:
        type, value, traceback = sys.exc_info()
        pass
    finally:
        fitFilesFile.close()

main()
