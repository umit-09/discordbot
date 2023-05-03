import hikari, psutil, lightbulb, random, time, os, json, asyncio, datetime, uvicorn, threading
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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

def fastapi_server():
    app = FastAPI()
    
    app.mount("/", StaticFiles(directory="."), name="files")

    @app.get("/")
    async def index():
        return FileResponse("index.html")

    uvicorn.run(app,host="0.0.0.0")

def hikari_server():
    with open('secret.secret', 'r') as f:
        bot = lightbulb.BotApp(token=f.readline().strip("\n"))

    from commands import addmod,addrole,addroleslot,bankinfo,banners,buybanner,buyrole,invite,on_guild_leave,on_started,ping,removemod,removerole,serverinfo,usebanner,vote
    bot.run()



thread1 = threading.Thread(target=fastapi_server)
thread2 = threading.Thread(target=hikari_server)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

try:
    while True:
        pass
except KeyboardInterrupt:
    thread1.stop()
    thread2.stop()