with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    
print("usebanner")

@bot.command
@lightbulb.option("bannername", "The name of the banner you want to purchase", type=str)
@lightbulb.command("usebanner", "Purchase a banner using your money", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def usebanner(
    ctx: lightbulb.SlashContext,
    bannername: str = None) -> None:

    user_id = ctx.author.id
    bank = read_list("bank.json")

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
            write_list("bank.json",bank)
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