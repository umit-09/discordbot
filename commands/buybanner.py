from main_V5 import bot
print("buybanner")

@bot.command
@lightbulb.option("bannername", "The name of the banner you want to purchase", type=str)
@lightbulb.command("buybanner", "Purchase a banner using your money", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def buybanner(
    ctx: lightbulb.SlashContext,
    bannername: str = None) -> None:

    user_id = ctx.author.id

    banners = read_list("banner.json")
    bank = read_list("bank.json")

    
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
        
        if bannername not in bank[str(user_id)]['banner']:
            
            if bank[str(user_id)]['balance'] >= count:
                
                balance = int(bank[str(user_id)]['balance'])
                bank[str(user_id)]['balance'] = balance - count

                bank[str(user_id)]["banner"] = bannername

                balance -= count

                if isinstance(bank[str(user_id)]['banner'], list):
                    bank[str(user_id)]['banner'].append(bannername)
                else:
                    bank[str(user_id)]['banner'] = [bank[str(user_id)]['banner'], bannername]
                
                write_list("bank.json", bank)
                
                write_list("bank.json", bank)
                await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"<@{user_id}> banner gived\nnow you have **{balance}{papir}**",
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
        return        
    else:
        
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you dont have an account yet, use **/vote** to get money",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return