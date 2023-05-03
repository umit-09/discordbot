with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    
print("buyrole")

@bot.command
@lightbulb.option("rolename", "The name of the role you want to purchase", type=hikari.Role)
@lightbulb.command("buyrole", "Purchase a role using your money", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def buyrole(
    ctx: lightbulb.SlashContext,
    rolename: Optional[hikari.Role] = None,) -> None:

    server_id = str(ctx.guild_id)
    user_id = ctx.author.id

    data = read_list("data.json")
    bank = read_list("bank.json")

    try:
        count = int(data[server_id]["roles"][str(rolename.id)])
    except:
        # Send the embed message
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> this role is not in sale",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    user_roles = [role.id for role in ctx.member.get_roles()]

    if str(user_id) in bank:
        if rolename.id not in user_roles:
            if bank[str(user_id)]['balance'] >= count:
                balance = int(bank[str(user_id)]['balance'])
                bank[str(user_id)]['balance'] = balance - count
                balance -= count

                write_list("bank.json",bank)
            
                await ctx.respond(hikari.Embed(
                    title=None,
                    description=f"<@{user_id}> role gived\nnow you have {balance}{papir}",
                    colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
                await bot.rest.add_role_to_member(user=user_id, guild=ctx.guild_id, role=rolename.id)
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
                description=f"<@{user_id}> you already have this role",
                colour=random.randint(0, 0xFFFFFF)))
            return
    else:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you dont have an account yet, use **/vote** to get money",
            colour=random.randint(0, 0xFFFFFF)))
        return