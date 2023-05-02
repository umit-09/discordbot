from main_V5 import bot
print("balance")

@bot.command()
@lightbulb.command("balance", "Get your inventory")
@lightbulb.implements(lightbulb.SlashCommand)
async def balance(ctx):
    # Get the user's ID, username, and the current time
    user_id = str(ctx.author.id)
    bank = read_list('bank.json')

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
        