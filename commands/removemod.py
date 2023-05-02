from main_V5 import bot
print("removemod")

@bot.command
@lightbulb.option("username", "select an moderator to remove", type=hikari.User)
@lightbulb.command("removemod", "remove a moderator!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def removemod(
    ctx: lightbulb.SlashContext,
    username: Optional[hikari.User] = None) -> None:

    user_id = ctx.member.id
    server_id = str(ctx.guild_id)

    data = read_list("data.json")

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
        write_list("data.json",data)
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{username.id}> is now not a moderator",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return