from main_V5 import bot
print("ping")

@bot.command()
@lightbulb.command("ping", "Get the current status of the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    # Get bot status information
    ping_time = f"{bot.heartbeat_latency*1000:.0f}ms"
    servers = sum(1 for _ in await bot.rest.fetch_my_guilds())
    ram_usage = f"{psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2:.2f}MB"
    data_size = f"{(os.path.getsize('./bank.json') + os.path.getsize('./data.json')) / 1024:.2f}KB"

    # Send the embed message
    await ctx.respond(hikari.Embed(
        title="Pong :ping_pong:",
        description=f"ping: **{ping_time}** \nservers: **{servers}** \nram usage: **{ram_usage}** \ndata size: **{data_size}**",
        colour=random.randint(0, 0xFFFFFF)))