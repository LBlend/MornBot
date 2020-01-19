from discord.ext import commands
import discord

from codecs import open
import yaml
import pymongo

from os import listdir
import locale
from time import time


locale.setlocale(locale.LC_ALL, '')

with open('config.yaml', 'r', encoding='utf8') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)


class MornBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(config['bot']['prefix']), case_insensitive=True)

        self.prefix = config['bot']['prefix']
        self.presence = config['bot']['presence']
        self.presence_activity = config['bot']['presence_activity']
        self.api_keys = config.get('api', {})
        self.emoji = config.get('emoji', {})
        self.misc = config.get('misc', {})
        self.database = config['database']


bot = MornBot()


activities = {
    'playing': 0,
    'listening': 2,
    'watching': 3
}
if bot.presence_activity.lower() in activities:
    activity_type = activities[bot.presence_activity]
else:
    activity_type = 0

requirements = {
    'FunReplies': bot.database,
    'Ordsky': bot.database,
    'osu': bot.api_keys['osu_api_key'],
    'Reddit': [bot.api_keys['reddit_client_id'], bot.api_keys['reddit_secret']],
    'Vær': bot.api_keys['openweathermap_api_key']
}


@bot.event
async def on_ready():
    if not hasattr(bot, 'uptime'):
        bot.uptime = time()

    for file in listdir('cogs'):
        if file.endswith('.py'):
            name = file[:-3]
            try:
                required = requirements[name]
                if required is None:
                    print(f'Slo av {name} pga manglende verdi satt i config.yaml')
                    continue
                if type(required) is list:
                    for requirement in required:
                        if requirement is None:
                            print(f'Slo av {name} pga manglende verdi satt i config.yaml')
                            continue
            except KeyError:
                pass
            bot.load_extension(f'cogs.{name}')

    print(f'\nBrukernavn:      {bot.user.name}')
    print(f'ID:              {bot.user.id}')
    print(f'Version:         {discord.__version__}')
    print('...............................................................\n')
    await bot.change_presence(activity=discord.Activity(type=activity_type, name=bot.presence),
                              status=discord.Status.online)

database_col_cog_check = pymongo.MongoClient(bot.database)['mornbot']['cog_check']


@bot.check
async def cog_blacklist(ctx):
    cog_check = database_col_cog_check.find_one({'_id': ctx.guild.id})
    try:
        return ctx.cog.qualified_name not in cog_check['disabled']
    except TypeError:
        return True
    except AttributeError:
        return True
    except KeyError:
        return True


bot.run(config['bot']['token'], bot=True, reconnect=True)
