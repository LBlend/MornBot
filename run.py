import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from os import listdir
import locale
from time import time


locale.setlocale(locale.LC_ALL, '')

with open("config.json", "r", encoding="utf8") as f:
    config = json_load(f)
    token = config["token"]
    prefix = config["prefix"]
    presence = config["presence"]
    activity_type = config["presence_activity"]

activities = {
    "playing": 0,
    "listening": 2,
    "watching": 3
}
if activity_type.lower() in activities:
    activity_type = activities[activity_type]
else:
    activity_type = 0

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefix),
    prefix=prefix,
    case_insensitive=True)

for file in listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")


@bot.event
async def on_ready():

    if not hasattr(bot, "uptime"):
        bot.uptime = time()

    print(f'Brukernavn:      {bot.user.name}')
    print(f'ID:              {bot.user.id}')
    print(f'Version:         {discord.__version__}')
    print('...............................................................\n')
    await bot.change_presence(activity=discord.Activity(
        type=activity_type,
        name=presence),
        status=discord.Status.online)

bot.run(token, bot=True, reconnect=True)
