import discord
import codecs
import os
import json
import locale
from discord.ext import commands
import time


locale.setlocale(locale.LC_ALL, '')

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    token = config["token"]
    prefix = config["prefix"]
    presence = config["presence"]
    activityType = config["presenceActivity"]

activities = {
"playing": 0,
"listening": 2,
"watching": 3
}
if activityType.lower() in activities:
    activityType = activities[activityType]
else:
    activityType = 0

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), prefix=prefix, case_insensitive=True)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

@bot.event
async def on_ready():

    if not hasattr(bot, "uptime"):
        bot.uptime = time.time()

    print(f'Brukernavn:      {bot.user.name}')
    print(f'ID:              {bot.user.id}')
    print(f'Version:         {discord.__version__}')
    print('...................................................................\n')
    await bot.change_presence(activity=discord.Activity(type=activityType, name=presence), status=discord.Status.online)

bot.run(token, bot=True, reconnect=True)