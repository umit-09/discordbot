from main_V5 import bot
print("addmod")

@bot.command
@lightbulb.option("username", "select an user to make mod", type=hikari.User)
@lightbulb.command("addmod", "Add a moderator!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def addmod(
    ctx: lightbulb.SlashContext,
    username: Optional[hikari.User] = None) -> None:

    user_id = ctx.member.id
    server_id = str(ctx.guild_id)

    data = read_list("data.json")

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
        
    write_list("data.json",data)

    await ctx.respond(hikari.Embed(
        title=None,
        description=f"<@{username.id}> is now a moderator",
        colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
