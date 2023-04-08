# this code made by umittadelen#4072
#        main V4.6
# ©      copyright 
#   all rights reserved

import hikari,psutil,lightbulb,random,time,os,json,asyncio
from typing import Optional
import datetime

coin = ["<:1:1084777301612437504>","<:2:1084777303223062609>","<:3:1084777306691731527>","<:4:1084777309103468584>","<:5:1084777310932193300>"]
papir = "<:papir:1084796977767776256>"
testers = ["852235304965242891","1086242607933440030","755088653835042906"]
data = {}
cooldown_time = 12 * 60 * 60

with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline())


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
    bank = read_list('bank.bin')
except:
    write_list('bank.bin',{})

try:
    data = read_list('data.bin')
except:
    write_list('data.bin',{})

# Define an event listener for when the bot starts
@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print(f'bot has started!')
    while True:
        bank = read_list("bank.bin")
        now = time.time()
        for user_id in list(bank.keys()):
            last_used = bank[user_id]["last_used"]
            delta = now - last_used
            if delta > 30 * 24 * 60 * 60: # 30 days in seconds
                # User has been inactive for a month or more, delete them
                del bank[user_id]
                write_list("bank.bin", bank)
            else:
                # Compute time remaining until deletion
                remaining = datetime.timedelta(seconds=30 * 24 * 60 * 60 - delta)
                days, seconds = remaining.days, remaining.seconds
                hours = seconds // 3600
                # Print time remaining for this user
        await asyncio.sleep(24 * 60 * 60)

@bot.listen()
async def on_guild_leave(event: hikari.GuildLeaveEvent) -> None:
    data = read_list("data.bin")
    if str(event.guild_id) in data:
        del data[str(event.guild_id)]
        write_list("data.bin",data)

@bot.command()
@lightbulb.command("vote", "Get daily money by voting for the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def vote(ctx):
    # Get the user's ID, username, and the current time
    user_id = str(ctx.author.id)
    now = time.time()
    reward = random.randint(1, 5)
    bank = read_list('bank.bin')

    # Check if the user has already used the command within the cooldown time
    if user_id in bank and (now - bank[user_id]['last_used']) < cooldown_time and user_id not in testers:
        time_left = int(cooldown_time - (now - bank[user_id]['last_used']))
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}>, you you already get your {papir}. \nTry again in **{time_left // 3600}H {(time_left % 3600) // 60}M**.\nyou have {bank[user_id]['balance']}{papir}",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return  
    
    # Update the user's balance in the bank data
    if user_id in bank:
        bank[user_id]['balance'] += reward
        bank[user_id]['last_used'] = now

    else:
        bank[user_id] = {'balance': reward, 'last_used': now, "banner": ["0"],"currentbanner":"0"}

    await ctx.respond(hikari.Embed(
        title=None,
        description=f"<@{user_id}>, you received **{reward}{coin[reward-1]}**! \nNow you have **{bank[user_id]['balance']}{papir}**.",
        colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))


    write_list("bank.bin",bank)

@bot.command()
@lightbulb.command("ping", "Get the current status of the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    # Get bot status information
    ping_time = f"{bot.heartbeat_latency*1000:.0f}ms"
    servers = sum(1 for _ in await bot.rest.fetch_my_guilds())
    ram_usage = f"{psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:.2f}MB"
    data_size = f"{(os.path.getsize('./bank.bin') + os.path.getsize('./data.bin')) / 1024:.2f}KB"

    # Send the embed message
    await ctx.respond(hikari.Embed(
        title="Pong :ping_pong:",
        description=f"ping: **{ping_time}** \nservers: **{servers}** \nram usage: **{ram_usage}** \ndata size: **{data_size}**",
        colour=random.randint(0, 0xFFFFFF)))


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

@bot.command
@lightbulb.option("rolename", "The name of the role you want to purchase", type=hikari.Role)
@lightbulb.command("buyrole", "Purchase a role using your money", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def buyrole(
    ctx: lightbulb.SlashContext,
    rolename: Optional[hikari.Role] = None,) -> None:

    server_id = str(ctx.guild_id)
    user_id = ctx.author.id

    data = read_list("data.bin")
    bank = read_list("bank.bin")

    try:
        count = int(data[server_id]["roles"][str(rolename.id)])
    except:
        # Send the embed message
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> this role is not in sale",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    user_roles = [role.id for role in ctx.member.get_roles()]

    if str(user_id) in bank:
        if rolename.id not in user_roles:
            if bank[str(user_id)]['balance'] >= count:
                balance = int(bank[str(user_id)]['balance'])
                bank[str(user_id)]['balance'] = balance - count
                balance -= count

                write_list("bank.bin",bank)
            
                await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"<@{user_id}> role gived\nnow you have {balance}{papir}",
                    colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
                await bot.rest.add_role_to_member(user=user_id, guild=ctx.guild_id, role=rolename.id)
                return
            else:
                await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"<@{user_id}> you dont have {count}{papir}",
                    colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
                return
        else:
            await ctx.respond(hikari.Embed(
                title=None,
                description=f"<@{user_id}> you already have this role",
                colour=random.randint(0, 0xFFFFFF)))
            return
    else:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you dont have an account yet, use **/vote** to get money",
            colour=random.randint(0, 0xFFFFFF)))
        return
    
@bot.command
@lightbulb.option("price", "The price of the role you want to add", type=str)
@lightbulb.option("rolename",  "The name of the role you want to add", type=hikari.Role)
@lightbulb.command("addrole", "Add a new role to the server with a specified price", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def addrole(
    ctx: lightbulb.SlashContext,
    price: str,
    rolename: Optional[hikari.Role] = None) -> None:

    server_id = str(ctx.guild_id)
    role_id = str(rolename.id)
    user_id = ctx.member.id

    data = read_list("data.bin")
    bank = read_list("bank.bin")

    if(server_id not in data):
        data = {server_id:{"roles":{},"mods":[]}}
    
    if(ctx.get_guild().owner_id not in data[server_id]["mods"]):
        data[server_id]["mods"].append(ctx.get_guild().owner_id)

    write_list("data.bin",data)

    if(user_id != ctx.get_guild().owner_id or user_id not in data[server_id]["mods"]):
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you need to be a moderator for use this command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    try:
        price = int(price)
    except:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> enter only numbers not characters",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return

    if ctx.member.id in data[server_id]["mods"] or user_id == ctx.get_guild().owner_id:
        try:
            if role_id in data[server_id]["roles"]:

                data[server_id]["roles"][role_id] = price
                write_list("data.bin",data)

                await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"<@&{role_id}> is already saved before.\n<@&{role_id}> is now **{data[server_id]['roles'][role_id]}{papir}**",
                    colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
                return
        except:
            print('something went wrong')

        else:
            if server_id not in data:
                data[server_id] = {"roles":{},"mods":[ctx.get_guild().owner_id]}

            if str(role_id) not in data[server_id]["roles"]:
                data[server_id]["roles"] = {role_id:price}
                
            write_list("data.bin",data)
            print("server saved to data.json")
            await ctx.respond(hikari.Embed(
                title=None,
                description=f"<@&{role_id}> added: **{price}{papir}**",
                colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
    else:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}>you need to be a moderator to use this command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))

@bot.command
@lightbulb.option("username", "select an user to make mod", type=hikari.User)
@lightbulb.command("addmod", "Add a moderator!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def addmod(
    ctx: lightbulb.SlashContext,
    username: Optional[hikari.User] = None) -> None:

    user_id = ctx.member.id
    server_id = str(ctx.guild_id)

    data = read_list("data.bin")

    if(user_id != ctx.get_guild().owner_id):
        print(user_id)
        print(ctx.get_guild().owner_id)
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{username.id}> you need to be a moderator for use this command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return

    if server_id not in data:
        data[server_id] = {"roles":{},"mods":[ctx.get_guild().owner_id]}

    if username.id not in data[server_id]["mods"]:
        data[server_id]["mods"].append(username.id)

    else:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{username.id}> is allready a moderator",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
        
    write_list("data.bin",data)

    await ctx.respond(hikari.Embed(
        title=None,
        description=f"<@{username.id}> is now a moderator",
        colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))

@bot.command
@lightbulb.option("username", "select an moderator to remove", type=hikari.User)
@lightbulb.command("removemod", "remove a moderator!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def removemod(
    ctx: lightbulb.SlashContext,
    username: Optional[hikari.User] = None) -> None:

    user_id = ctx.member.id
    server_id = str(ctx.guild_id)

    data = read_list("data.bin")

    if user_id != ctx.get_guild().owner_id:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you need to be a moderator for use this command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    if username.id == ctx.get_guild().owner_id:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{username.id}> you cannot delete the server creator",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return

    if ctx.get_guild().owner_id not in data[server_id]["mods"]:
        data[server_id]["mods"].append(ctx.get_guild().owner_id)

    if server_id not in data:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{username.id}> this server is not saved before you need to run **/addrole** command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    if username.id not in data[server_id]["mods"]:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{username.id}> is not a moderator",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return

    else:
        data[server_id]["mods"].remove(username.id)
        write_list("data.bin",data)
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{username.id}> is now not a moderator",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
@bot.command()
@lightbulb.command("balance", "Get your inventory")
@lightbulb.implements(lightbulb.SlashCommand)
async def balance(ctx):
    # Get the user's ID, username, and the current time
    user_id = str(ctx.author.id)
    bank = read_list('bank.bin')

    if user_id not in bank:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you dont have an account yet use **/vote** to get money and account",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    else:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"**<@{user_id}>'s account:**\n• balance: **{bank[user_id]['balance']}**{papir}\n• last used: **{datetime.fromtimestamp(bank[user_id]['last_used'])}**",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        
@bot.command
@lightbulb.option("rolename",  "The name of the role you want to add", type=hikari.Role)
@lightbulb.command("removerole", "Add a new role to the server with a specified price", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def removerole(
    ctx: lightbulb.SlashContext,
    rolename: Optional[hikari.Role] = None) -> None:

    user_id = ctx.member.id
    server_id = str(ctx.guild_id)

    if user_id != ctx.get_guild().owner_id:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you need to be a moderator for use this command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    if(user_id != ctx.get_guild().owner_id or user_id not in data[server_id]["mods"]):
        print(user_id,type(user_id))
        print(ctx.get_guild().owner_id,type(ctx.get_guild().owner_id))
        print(data[server_id]["mods"])
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you need to be a moderator for use this command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    if str(rolename.id) in data[server_id]["roles"]:
        del data[server_id]["roles"][str(rolename.id)]
        write_list("data.bin",data)

        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@&{rolename.id}> is deleted",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    else:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"there is not a saved role named <@&{rolename.id}>",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        
@bot.command()
@lightbulb.command("serverinfo", "Get server information")
@lightbulb.implements(lightbulb.SlashCommand)
async def serverinfo(ctx: lightbulb.SlashContext):
    # Get the user's ID, username, and the current time
    server_id = str(ctx.guild_id)
    data = read_list('data.bin')
    roles = ""
    mods = ""

    if server_id in data:
        for a in data[server_id]["roles"]:
            roles = roles + f"• <@&{a}>: **{data[server_id]['roles'][a]}**\n"
        for b in data[server_id]["mods"]:
            mods = mods + f"• <@{b}>\n"

        await ctx.respond(hikari.Embed(
            title=None,
            description=f"**roles:**\n{roles}\n\n**moderators:**\n{mods}",
            colour=random.randint(0, 0xFFFFFF)))
    else:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"this server has nothing",
            colour=random.randint(0, 0xFFFFFF)))
        
@bot.command()
@lightbulb.command("bankinfo", "Get your information")
@lightbulb.implements(lightbulb.SlashCommand)
async def serverinfo(ctx: lightbulb.SlashContext):
    user_id = ctx.author.id
    await ctx.respond(hikari.Embed(
        title="Link",
        description=f"<@{user_id}> your account information is here",
        colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None,
        url=f"https://umit-09.github.io/discordbot/bank.html?id={user_id}"))
    
@bot.command
@lightbulb.option("bannername", "The name of the banner you want to purchase", type=str)
@lightbulb.command("buybanner", "Purchase a banner using your money", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def buybanner(
    ctx: lightbulb.SlashContext,
    bannername: str = None) -> None:

    user_id = ctx.author.id

    banners = read_list("banner.bin")
    bank = read_list("bank.bin")

    
    if str(user_id) in bank:
        
        try:
            count = int(banners[bannername])
        except:
            # Send the embed message
            await ctx.respond(hikari.Embed(
                title=None,
                description=f"<@{user_id}> this banner is not in sale",
                colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
            return

        if isinstance(bank[str(user_id)]['banner'], list):
            bank[str(user_id)]['banner'].append(bannername)
        else:
            bank[str(user_id)]['banner'] = [bank[str(user_id)]['banner'], bannername]
        
        write_list("bank.bin", bank)
        
        if bannername not in bank[str(user_id)]['banner']:
            
            if bank[str(user_id)]['balance'] >= count:
                
                balance = int(bank[str(user_id)]['balance'])
                bank[str(user_id)]['balance'] = balance - count

                bank[str(user_id)]["banner"] = bannername

                balance -= count
                
                write_list("bank.bin", bank)
                await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"<@{user_id}> banner gived\nnow you have {balance}{papir}",
                    colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
                return
            
            else:
                
                await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"<@{user_id}> you dont have {count}{papir}",
                    colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
                return
            
        else:
            
            await ctx.respond(hikari.Embed(
                title=None,
                description=f"<@{user_id}> you already have this banner",
                colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
            return
        
    else:
        
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you dont have an account yet, use **/vote** to get money",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return


@bot.command
@lightbulb.option("bannername", "The name of the banner you want to purchase", type=str)
@lightbulb.command("usebanner", "Purchase a banner using your money", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def usebanner(
    ctx: lightbulb.SlashContext,
    bannername: str = None) -> None:

    user_id = ctx.author.id
    bank = read_list("bank.bin")

    if str(user_id) in bank:
        
        try:
            print(bank[str(user_id)]["banner"])
        except:
            await ctx.respond(hikari.Embed(
                title=None,
                description=f"<@{user_id}> you dont have an account yet, use **/vote** to get money",
                colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
            return
        
        if bannername in bank[str(user_id)]["banner"]:
            bank[str(user_id)]["currentbanner"] = bannername
            write_list("bank.bin",bank)
            await ctx.respond(hikari.Embed(
                title=None,
                description=f"<@{user_id}> now you are using {bannername}",
                colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
            return

        else:

            await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"<@{user_id}> you dont have that banner use **/buybanner** to buy",
                    colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
    
    else:
        
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you dont have an account yet, use **/vote** to get money",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return


# Run the bot
bot.run()