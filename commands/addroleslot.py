with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    
print("addroleslot")

@bot.command()
@lightbulb.command("addroleslot", "Add 2 role slot with 30")
@lightbulb.implements(lightbulb.SlashCommand)
async def addroleslot(ctx: lightbulb.SlashContext):
    user_id = ctx.member.id
    server_id = str(ctx.guild_id)
    data = read_list("data.json")
    bank = read_list("bank.json")

    if(server_id not in data):
        data = {server_id:{"roles":{},"mods":[],"max_roles":5}}
    
    if(user_id != ctx.get_guild().owner_id or user_id not in data[server_id]["mods"]):
        print(user_id,type(user_id))
        print(ctx.get_guild().owner_id,type(ctx.get_guild().owner_id))
        print(data[server_id]["mods"])
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you need to be a moderator for use this command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    if str(user_id) in bank:
        count = 30
        if bank[str(user_id)]['balance'] >= count:
            balance = int(bank[str(user_id)]['balance'])
            bank[str(user_id)]['balance'] = balance - count
            balance -= count

            data[server_id]["max_roles"] = data[server_id]["max_roles"] + 2
            write_list("bank.json",bank)
            write_list("data.json",data)
        
            await ctx.respond(hikari.Embed(
                title=None,
                description=f"<@{user_id}> 2 role slot added,\nnow you have {balance}{papir}\nnow this server has {data[server_id]['max_roles']} slots",
                colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
            return
        else:
            await ctx.respond(hikari.Embed(
                title=None,
                description=f"<@{user_id}> you dont have {count}{papir}",
                colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
            return