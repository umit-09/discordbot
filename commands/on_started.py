with open('secret.secret', 'r') as f:
    bot = lightbulb.BotApp(token=f.readline().strip("\n"))
    
print("on_started")

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print(f'bot has started!')
    while True:
        bank = read_list("bank.json")
        now = time.time()
        for user_id in list(bank.keys()):
            last_used = bank[user_id]["last_used"]
            delta = now - last_used
            if delta > 30 * 24 * 60 * 60: # 30 days in seconds
                # User has been inactive for a month or more, delete them
                del bank[user_id]
                write_list("bank.json", bank)
            else:
                # Compute time remaining until deletion
                remaining = datetime.timedelta(seconds=30 * 24 * 60 * 60 - delta)
                days, seconds = remaining.days, remaining.seconds
                hours = seconds // 3600
                # Print time remaining for this user
        await asyncio.sleep(24 * 60 * 60)