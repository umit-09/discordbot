# this code made by umittadelen#4072
#         main V5
# ©      copyright 
#   all rights reserved

import hikari,psutil,lightbulb,random,time,os,json,asyncio,datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

coin = ["<:1:1084777301612437504>","<:2:1084777303223062609>","<:3:1084777306691731527>","<:4:1084777309103468584>","<:5:1084777310932193300>"]
papir = "<:papir:1084796977767776256>"
testers = ["852235304965242891","1086242607933440030","755088653835042906"]
cooldown_time = 12 * 60 * 60

with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
app = FastAPI()

def read_list(file):
    try:
        with open(file, 'r') as fp:
            output = json.load(fp)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        output = {}
    print(f"\n\n{file}:\n")
    print(json.dumps(output, indent=4))
    return output

# Starts the bot when the server starts
@app.on_event("startup")
async def on_startup() -> None:
    await bot.start()

# Closes the bot when the server closes
@app.on_event("shutdown")
async def on_shutdown() -> None:
    await bot.close()

@app.get("/")
async def index() -> JSONResponse:
    return JSONResponse(read_list("./bank.json"))

# Mount the static directory to the app
app.mount("/static", StaticFiles(directory="."), name="static")

# Run the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="84.211.187.101", port=8000)