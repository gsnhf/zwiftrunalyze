
import aiohttp
import aiofiles as aiof
import logging

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
                    log(runtoken)
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