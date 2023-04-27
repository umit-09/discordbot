# this code made by umittadelen#4072
#         main V5
# ©      copyright 
#   all rights reserved

import hikari,psutil,lightbulb,random,time,os,json,asyncio,datetime,uvicorn
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

###################### define (start) ###########################

coin = ["<:1:1084777301612437504>","<:2:1084777303223062609>","<:3:1084777306691731527>","<:4:1084777309103468584>","<:5:1084777310932193300>"]
papir = "<:papir:1084796977767776256>"
testers = ["852235304965242891","1086242607933440030","755088653835042906"]
cooldown_time = 12 * 60 * 60

def write_list(file, input):
    with open(file, 'w') as fp:
        json.dump(input, fp)
    print(f"\n\n{file}:\n")
    print(json.dumps(input, indent=4))

# Read list from JSON file
def read_list(file):
    try:
        with open(file, 'r') as fp:
            output = json.load(fp)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        output = {}
    print(f"\n\n{file}:\n")
    print(json.dumps(output, indent=4))
    return output

try:
    bank = read_list('bank.json')
except:
    write_list('bank.json',{})

try:
    data = read_list('data.json')
except:
    write_list('data.json',{})

###################### define (end) ###########################

###################### start (start) ###########################

app = FastAPI()
# Mount the static directory to the app
app.mount("/static", StaticFiles(directory="."), name="static")

with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))

# Starts the bot when the server starts
@app.on_event("startup")
async def on_startup() -> None:
    await bot.start()

# Closes the bot when the server closes
@app.on_event("shutdown")
async def on_shutdown() -> None:
    await bot.close()

###################### start (end) ###########################

###################### webserver (start) ###########################

@app.get("/bank")
async def index() -> JSONResponse:
    return JSONResponse(read_list("./bank.json"))

###################### webserver (end) ###########################

###################### hikari (start) ###########################
@bot.command()
@lightbulb.command("invite", "Get an invite link for the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def invite(ctx):

    # Send the embed message
    await ctx.respond(hikari.Embed(
        title="Link",
        description=f"you can use this link to invite me to any server\nplease don't spam",
        colour=random.randint(0, 0xFFFFFF),
        url="https://discord.com/api/oauth2/authorize?client_id=1084422933805535312&permissions=8&scope=bot"))
###################### hikari (end) ###########################

uvicorn.run(app, host="localhost", port=8000)
#ssh umittadelen@84.211.187.101