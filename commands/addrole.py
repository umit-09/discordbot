from main_V5 import bot
print("addrole")

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

    data = read_list("data.json")
    bank = read_list("bank.json")

    if(server_id not in data):
        data = {server_id:{"roles":{},"mods":[],"max_roles":5}}
    
    if(ctx.get_guild().owner_id not in data[server_id]["mods"]):
        data[server_id]["mods"] += ctx.get_guild().owner_id

    write_list("data.json",data)

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
                if len(data[server_id]["roles"]) < data[server_id]["max_roles"]:
                    data[server_id]["roles"][role_id] = price
                else:
                    await ctx.respond(hikari.Embed(
                        title=None,
                        description=f"The server's role limit has been reached. Use the /addroleslot command to add a new role.",
                        colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
                    return
                write_list("data.json",data)

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

            if len(data[server_id]["roles"]) < data[server_id]["max_roles"]:
                data[server_id]["roles"][role_id] = price
            else:
                await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"The server's role limit has been reached. Use the /addroleslot command to add a new role.",
                    colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
                return
                
            write_list("data.json",data)
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