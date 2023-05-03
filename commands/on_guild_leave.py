with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    
print("on_guild_leave")

@bot.listen()
async def on_guild_leave(event: hikari.GuildLeaveEvent) -> None:
    data = read_list("data.json")
    if str(event.guild_id) in data:
        del data[str(event.guild_id)]
        write_list("data.json",data)