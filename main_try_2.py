import hikari, psutil, lightbulb, random, time, os, json, asyncio, datetime, uvicorn
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import concurrent.futures

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
def task_one():
    app = FastAPI()
    # Mount the static directory to the app
    app.mount("/static", StaticFiles(directory="."), name="static")

    with open('secret.secret', 'r') as f:
        bot = lightbulb.BotApp(token=f.readline().strip("\n"))

    @app.get("/bank")
    async def index() -> JSONResponse:
        return JSONResponse(read_list("./bank.json"))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(uvicorn.run(app, loop=loop, port=8000))

def task_two():
    with open('secret.secret', 'r') as f:
        bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    from commands import addmod,addrole,addroleslot,balance,bankinfo,banners,buybanner,buyrole,invite,on_guild_leave,on_started,ping,removemod,removerole,serverinfo,usebanner,vote
    bot.run()

async def main():
    async with asyncio.get_running_loop() as loop:
        task1 = loop.create_task(task_one())
        task2 = loop.create_task(task_two())
        await asyncio.gather(task1, task2)

asyncio.run(main())