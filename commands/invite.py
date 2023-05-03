with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    
print("invite")

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