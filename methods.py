
import aiofiles as aiof
import aiohttp
import asyncio
import logging
import sys

def log(message):
    logging.info(message)

def logError(message):
    logging.error(message)

async def write_fitFile(fileName, response):
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

async def upload(session, fileName, runtoken):
    try:
        log(runtoken)
        async with session.post("https://runalyze.com/api/v1/activities/uploads", data={'file': open(fileName, "rb")}, headers={"token": runtoken}) as responsePost:
            log("post finished: " + str(responsePost.text))
    except:
        type, value, traceback = sys.exc_info()
        logError("runalyze error: " + str(value))
        pass

async def uploadToRunalyze(link, fileName, runtoken, sessionKey):
    try:
      async with aiohttp.ClientSession() as session:
        cookies = {
         'mywhooshweb_session': sessionKey
        }
        async with session.get(link, cookies=cookies) as response:
            await write_fitFile(fileName, response)
            if runtoken:
                await upload(session, fileName, runtoken)
                
    except:
        type, value, traceback = sys.exc_info()
        logError(str(value))
        pass