# this code made by umittadelen#4072

# ©      copyright 
#   all rights reserved

# Import necessary modules
import hikari,psutil,lightbulb,random,json,time,os
from typing import Optional

coin = ["<:1:1084777301612437504>","<:2:1084777303223062609>","<:3:1084777306691731527>","<:4:1084777309103468584>","<:5:1084777310932193300>"]
papir = "<:papir:1084796977767776256>"
testers = ["852235304965242891","1086242607933440030"]
data = {"servers":{}}
cooldown_time = 12 * 60 * 60

with open('.gitignore', 'r') as f:
    TOKENa = f.readline()
    print(TOKENa)

bot = lightbulb.BotApp(token=TOKENa)   

# Load existing bank data from a JSON file
bank = {}
with open('bank.json', 'r') as f:
    bank = json.load(f)

# Define an event listener for when the bot starts
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print(f'bot has started!')

# Define a command for getting daily money
@bot.command()
@lightbulb.command("vote", "vote for get daily money")
@lightbulb.implements(lightbulb.SlashCommand)
async def vote(ctx):
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
    print("someone voted: ",bank)

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

@bot.command
@lightbulb.option("rolename", "sellected role", type=hikari.Role)
@lightbulb.command("role", "Make an announcement!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def role(
    ctx: lightbulb.SlashContext,
    rolename: Optional[hikari.Role] = None,) -> None:
    with open('data.json', 'r') as f:
        data = json.load(f)

    try:
        count = int(data["roles"][str(rolename.id)])
    except:
        await ctx.respond(f"{ctx.member} this role is not in sale")
        return

    user_roles = [role.id for role in ctx.member.get_roles()]

    if str(ctx.author.id) in bank:
        if rolename.id not in user_roles:
            if bank[str(ctx.member.id)]['balance'] >= count:
                balance = int(bank[str(ctx.member.id)]['balance'])
                bank[str(ctx.member.id)]['balance'] = balance - count
                balance -= count

                with open('bank.json', 'w') as f:
                    json.dump(bank, f)
                
                await ctx.respond(f"role gived\nnow you have {balance}{papir}")
                await bot.rest.add_role_to_member(user=ctx.member.id, guild=ctx.guild_id, role=rolename.id)
                return
            else:
                await ctx.respond(f"{ctx.member} you dont have {count}{papir}")
                return
        else:
            await ctx.respond(f"{ctx.member} you already have this role")
            return
    else:
        await ctx.respond(f"{ctx.member} you dont have an account yet, use /vote to get money")
        return

@bot.command
@lightbulb.option("price", "selected role price", type=str)
@lightbulb.option("rolename", "selected role", type=hikari.Role)
@lightbulb.command("addrole", "Add a role to the server!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def addrole(
    ctx: lightbulb.SlashContext,
    price: str,
    rolename: Optional[hikari.Role] = None) -> None:

    server_id = str(ctx.guild_id)
    role_id = str(rolename.id)

    if(ctx.member.id != ctx.get_guild().owner_id or ctx.member.id not in data["moderators"][server_id]):
        await ctx.respond("you need to be a moderator for use this command")
        return
    
    with open('data.json', 'r') as f:
        data = json.load(f)
        
    try:
        price = int(price)
    except:
        await ctx.respond(f"{ctx.member} enter only numbers not chaaracters")
        return

    if ctx.member.id in data["moderators"][server_id]:
        try:
            if role_id in data["roles"]:

                with open('data.json', 'w') as f:
                    data["roles"] = {role_id:price}
                    json.dump(data, f)
                await ctx.respond(f"{'<@&' + role_id + '>'} is already saved before.\n{'<@&' + role_id + '>'} is now **{data['roles'][role_id]}{papir}**")
                return
        except:
            with open('bank.json', 'w') as f:
                json.dump({"roles":{},"moderators":{}}, f)
                print(data["roles"])

                with open('data.json', 'w') as f:
                    data["roles"] = {role_id:price}
                    json.dump(data, f)

        else:
            with open('data.json', 'w') as f:

                if str(role_id) not in data["roles"]:
                    data["roles"][role_id] = price
                    
                json.dump(data, f)
                print(data)
                print("server saved to data.json")
                await ctx.respond(f"{'<@&' + role_id + '>'} added: **{price}{papir}**")

@bot.command
@lightbulb.option("username", "select an user to make mod", type=hikari.User)
@lightbulb.command("addmod", "Add a moderator!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def addrole(
    ctx: lightbulb.SlashContext,
    username: Optional[hikari.User] = None) -> None:

    with open('data.json', 'r') as f:
        data = json.load(f)

    server_id = str(ctx.guild_id)

    if(ctx.member.id != ctx.get_guild().owner_id or ctx.member.id not in data["moderators"][server_id]):
        await ctx.respond(f"{username} you need to be a moderator for use this command")
        return

    if "moderators" not in data:
        data["moderators"] = {}
    if server_id not in data["moderators"]:
        data["moderators"][server_id] = [ctx.get_guild().owner_id]
    if username.id not in data["moderators"][server_id]:
        data["moderators"][server_id].append(username.id)
    else:
        await ctx.respond(f"{username} is allready a moderator")
        return
        
    with open('data.json', 'w') as f:
        json.dump(data, f)

    await ctx.respond(f"<@&{username.id}> is now a moderator")

# Run the bot
bot.run()