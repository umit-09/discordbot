# Import necessary modules
import hikari,psutil,lightbulb,random,json,time,os
from typing import Optional

coin = ["<:1:1084777301612437504>","<:2:1084777303223062609>","<:3:1084777306691731527>","<:4:1084777309103468584>","<:5:1084777310932193300>"]
papir = "<:papir:1084796977767776256>"

testers = ["852235304965242891","891701105417932832"]

with open('secret.secret', 'r') as f:
    TOKENa = f.readline()

bot = lightbulb.BotApp(token=TOKENa)   

# Load existing bank data from a JSON file
bank = {}
with open('bank.json', 'r') as f:
    bank = json.load(f)

# Set the cooldown time in seconds
cooldown_time = 12 * 60 * 60

# Initialize the bot with a token


# Define an event listener for when the bot starts
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print(f'bot has started! {TOKENa}')

# Define a command for getting daily money
@bot.command()
@lightbulb.command("getmoney", "get daily money")
@lightbulb.implements(lightbulb.SlashCommand)
async def getmoney(ctx):
    # Get the user's ID, username, and the current time
    user_id = str(ctx.author.id)
    username = ctx.author.username
    now = time.time()
    reward = random.randint(1, 5)

    # Check if the user has already used the command within the cooldown time
    if user_id in bank and (now - bank[user_id]['last_used']) < cooldown_time and user_id not in testers:
        time_left = int(cooldown_time - (now - bank[user_id]['last_used']))
        await ctx.respond(f"{username}, you you already get your {papir}. \nTry again in **{time_left // 3600}H {(time_left % 3600) // 60}M**.\nyou have {bank[user_id]['balance']}{papir}")
        return    
    
    # Update the user's balance in the bank data
    if user_id in bank:
        bank[user_id]['balance'] += reward
    else:
        bank[user_id] = {'balance': reward, 'last_used': now}

    await ctx.respond(f"{username}, you received **{reward}{coin[reward-1]}**! \nNow you have **{bank[user_id]['balance']}{papir}**.")

    # Update the user's last used time in the bank data and save it to the JSON file
    bank[user_id]['last_used'] = now
    with open('bank.json', 'w') as f:
        json.dump(bank, f)
    # Print the updated bank data to the console for debugging purposes
    print(bank)

# Define a command for checking the bot's status
@bot.command()
@lightbulb.command("ping", "get bot status")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    # Get bot status information
    ping_time = f"{bot.heartbeat_latency*1000:.0f}ms"
    servers = sum(1 for _ in await bot.rest.fetch_my_guilds())
    ram_usage = f"{psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:.2f}MB"
    data_size = f"{os.path.getsize('bank.json') / 1024:.2f}KB"

    # Format and send the bot status message
    message = f"ping: **{ping_time}** \nservers: **{servers}** \nram usage: **{ram_usage}** \ndata size: **{data_size}**"
    await ctx.respond(message)

@bot.command()
@lightbulb.command("invite", "get invite link")
@lightbulb.implements(lightbulb.SlashCommand)
async def invite(ctx):
    await ctx.respond("you can use this link to invite me to any server\nplease don't spam\nhttps://discord.com/api/oauth2/authorize?client_id=1084422933805535312&permissions=8&scope=bot")

# Run the bot
bot.run()
