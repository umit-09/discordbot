with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    
print("vote")

@lightbulb.command("vote", "Get daily money by voting for the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def vote(ctx):
    # Get the user's ID, username, and the current time
    user_id = str(ctx.author.id)
    now = time.time()
    reward = random.randint(1, 5)
    bank = read_list('bank.json')

    # Check if the user has already used the command within the cooldown time
    if user_id in bank and (now - bank[user_id]['last_used']) < cooldown_time and user_id not in testers:
        time_left = int(cooldown_time - (now - bank[user_id]['last_used']))
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}>, you you already get your {papir}. \nTry again in **{time_left // 3600}H {(time_left % 3600) // 60}M**.\nyou have {bank[user_id]['balance']}{papir}",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return  
    
    # Update the user's balance in the bank data
    if user_id in bank:
        bank[user_id]['balance'] += reward
        bank[user_id]['last_used'] = now

    else:
        bank[user_id] = {'balance': reward, 'last_used': now, "banner": ["0"],"currentbanner":"0"}

    await ctx.respond(hikari.Embed(
        title=None,
        description=f"<@{user_id}>, you received **{reward}{coin[reward-1]}**! \nNow you have **{bank[user_id]['balance']}{papir}**.",
        colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))


    write_list("bank.json",bank)
