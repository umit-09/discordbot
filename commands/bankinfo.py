with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    
print("bankinfo")

@bot.command()
@lightbulb.command("bankinfo", "Get your information")
@lightbulb.implements(lightbulb.SlashCommand)
async def bankinfo(ctx: lightbulb.SlashContext):
    user_id = ctx.author.id
    await ctx.respond(hikari.Embed(
        title="Link",
        description=f"<@{user_id}> your account information is here",
        colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None,
        url=f"https://umit-09.github.io/discordbot/bank.html?id={user_id}"))