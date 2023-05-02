from main_V5 import bot
print("serverinfo")

@bot.command()
@lightbulb.command("serverinfo", "Get server information")
@lightbulb.implements(lightbulb.SlashCommand)
async def serverinfo(ctx: lightbulb.SlashContext):
    # Get the user's ID, username, and the current time
    server_id = str(ctx.guild_id)
    data = read_list('data.json')
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