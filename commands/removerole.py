from main_V5 import bot
print("removerole")

@bot.command
@lightbulb.option("rolename",  "The name of the role you want to add", type=hikari.Role)
@lightbulb.command("removerole", "Add a new role to the server with a specified price", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand) 
async def removerole(
    ctx: lightbulb.SlashContext,
    rolename: Optional[hikari.Role] = None) -> None:

    user_id = ctx.member.id
    server_id = str(ctx.guild_id)
    
    if(user_id != ctx.get_guild().owner_id or user_id not in data[server_id]["mods"]):
        print(user_id,type(user_id))
        print(ctx.get_guild().owner_id,type(ctx.get_guild().owner_id))
        print(data[server_id]["mods"])
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@{user_id}> you need to be a moderator for use this command",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    
    if str(rolename.id) in data[server_id]["roles"]:
        del data[server_id]["roles"][str(rolename.id)]
        write_list("data.json",data)

        await ctx.respond(hikari.Embed(
            title=None,
            description=f"<@&{rolename.id}> is deleted",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        return
    else:
        await ctx.respond(hikari.Embed(
            title=None,
            description=f"there is not a saved role named <@&{rolename.id}>",
            colour=random.randint(0, 0xFFFFFF)).set_image(f"./assets/banner/{bank[str(user_id)]['currentbanner']}.png" if str(user_id) in bank and bank[str(user_id)]['currentbanner'] != "0" else None))
        