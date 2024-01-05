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
    profile = client.get_profile()
    activities = client.get_activity(profile.profile["id"])
    activities = activities.list()

    # Import only after importdate
    if len(sys.argv) > 1:
        importdate = pd.to_datetime(sys.argv[1])
    else:
        importdate = pd.to_datetime(datetime.now())

    try:
        if not os.path.exists("data"):
            os.makedirs("data")

        with open("data/fitFiles.json", "w") as fitFilesFile:
            json.dump(activities, fitFilesFile, indent=2)

        for activity in activities:
            if pd.to_datetime(activity["endDate"]).tz_convert(None) > importdate:
                printText("Activity ended after set importdate. Skipping.")
                continue
            link = "https://" + activity["fitFileBucket"] + ".s3.amazonaws.com/" + activity["fitFileKey"]

            fNameShort = pd.to_datetime(activity["endDate"]).strftime("%Y%m%d_%H%M%S")

            fName = "data/" + fNameShort

            # fitFilesFile.write(fNameShort + "\n")

            if os.path.isfile(fName+".fit"):
                printText("Already downloaded. Skipping")
                continue

            printText("Processing: " + activity["name"] + " - Date: " + pd.to_datetime(activity["endDate"]).strftime("%Y-%m-%d") + " - " + str(activity["distanceInMeters"] / 1000) + "km")

            continue # das löschen

            # Save Fit File
            res = requests.get(link)
            with open(fName + ".fit", "wb") as f:
                f.write(res.content)
            # if runtoken:
                # r = requests.post("https://runalyze.com/api/v1/activities/uploads", files={'file': open(fname + ".fit", "rb")}, headers={"token": runtoken})
                # printText(r.text)
                
            # Save Desc Data as Json
            with open(fName+"_desc.json", "w") as f:
                json.dump(activity, f)
    except:
        pass
    finally:
        fitFilesFile.close()

main()
