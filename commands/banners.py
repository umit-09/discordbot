from main_V5 import bot
print("banners")

@bot.command()
@lightbulb.command("banners", "Get a link for the list of banners")
@lightbulb.implements(lightbulb.SlashCommand)
async def banners(ctx):
    # Send the embed message
    await ctx.respond(hikari.Embed(
        title="Link",
        description=f"you can use this link to view all of the banners",
        colour=random.randint(0, 0xFFFFFF),
        url="https://umit-09.github.io/discordbot/"))