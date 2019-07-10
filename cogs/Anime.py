import discord
from discord.ext import commands

from codecs import open
from json import load as json_load
from requests import post
from datetime import datetime
from re import sub

from cogs.utils import Defaults

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.group()
    async def anilist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)        

    @anilist.command()
    async def animeprofil(self, ctx, bruker: str):
        """Viser animeinformasjon til en Anilist-profil"""

        async with ctx.channel.typing():

            # GraphQL 
            query = """
            query ($name: String) {
                User (name: $name) {
                    name
                    siteUrl
                    updatedAt
                    avatar {
                        medium
                    }
                    options {
                        profileColor
                    }
                    stats {
                        watchedTime
                        animeStatusDistribution {
                            amount
                        }
                        animeListScores {
                            meanScore
                        }
                    }
                }
            }
            """
            variables = {
                'name': bruker
            }
            try:
                data = post(
                    'https://graphql.anilist.co',
                    json={'query': query, 'variables': variables}).json()
                user_url = data['data']['User']['siteUrl']
            except TypeError:
                return await Defaults.error_fatal_send(
                    ctx, text='Kunne ikke finne brukeren\n\n' +
                        f'Skriv `{prefix}help {ctx.command}` for hjelp',
                        mention=False)

            user_name = data['data']['User']['name']
            profile_pic = data['data']['User']['avatar']['medium']
            last_updated = data['data']['User']['updatedAt']
            last_updated = datetime.fromtimestamp(last_updated).strftime('%d.%m.%Y %H:%M')
            now = datetime.now().strftime('%d.%m.%Y %H:%M')
            days_watched = round(data['data']['User']['stats']['watchedTime'] / 1440, 1)
            watching = data['data']['User']['stats']['animeStatusDistribution'][0]['amount']
            planning = data['data']['User']['stats']['animeStatusDistribution'][1]['amount']
            completed = data['data']['User']['stats']['animeStatusDistribution'][2]['amount']
            dropped = data['data']['User']['stats']['animeStatusDistribution'][3]['amount']

            try:
                anime_mean_score = data['data']['User']['stats']['animeListScores']['meanScore']
            except TypeError:
                anime_mean_score = '**Ingen**'
            if not anime_mean_score:
                anime_mean_score = '**Ingen**'

            color = data['data']['User']['options']['profileColor']
            colors = {
                'blue': 0x3db4f2,
                'purple': 0xc063ff,
                'pink': 0xFC9DD6,
                'orange': 0xEF881A,
                'red': 0xE13333,
                'green': 0x4CCA51,
                'gray': 0x677B94
            }
            if color in colors:
                color = colors[color]
            else:
                color = 0x3db4f2

            embed = discord.Embed(title=user_name, color=color, url=user_url)
            embed.set_author(name='Anilist', icon_url='https://avatars3.githubusercontent.com/u/18018524?s=200&v=4')
            embed.set_thumbnail(url=profile_pic)
            embed.add_field(name='Gj.snittlig vurdering', value=anime_mean_score)
            embed.add_field(name='Antall dager sett', value=days_watched)
            embed.add_field(name='Antall animer sett', value=completed)
            embed.add_field(name='Ser på nå', value=watching)
            embed.add_field(name='Planlegger å se', value=planning)
            embed.add_field(name='Droppet', value=dropped)
            embed.set_footer(text=f'(Norske tider) Oppdatert: {last_updated} | Tid nå: {now}')
            await ctx.send(embed=embed)

    @anilist.command()
    async def mangaprofil(self, ctx, bruker: str):
        """Viser mnagainformasjonen til en Anilist-profil"""

        async with ctx.channel.typing():

            # GraphQL 
            query = """
            query ($name: String) {
                User (name: $name) {
                    name
                    siteUrl
                    updatedAt
                    avatar {
                        medium
                    }
                    options {
                        profileColor
                    }
                    stats {
                        chaptersRead
                        mangaStatusDistribution {
                            amount
                        }
                        mangaListScores {
                            meanScore
                        }
                    }
                }
            }
            """
            variables = {
                'name': bruker
            }

            try:
                data = post(
                    'https://graphql.anilist.co',
                    json={'query': query, 'variables': variables}).json()
                user_url = data['data']['User']['siteUrl']
            except TypeError:
                return await Defaults.error_fatal_send(
                    ctx, text='Kunne ikke finne brukeren\n\n' +
                        f'Skriv `{prefix}help {ctx.command}` for hjelp')

            user_name = data['data']['User']['name']
            profile_pic = data['data']['User']['avatar']['medium']
            last_updated = data['data']['User']['updatedAt']
            last_updated = datetime.fromtimestamp(last_updated).strftime('%d.%m.%Y %H:%M')
            now = datetime.now().strftime('%d.%m.%Y %H:%M')
            chapters_read = data['data']['User']['stats']['chaptersRead']
            reading = data['data']['User']['stats']['mangaStatusDistribution'][0]['amount']
            planning = data['data']['User']['stats']['mangaStatusDistribution'][1]['amount']
            completed = data['data']['User']['stats']['mangaStatusDistribution'][2]['amount']
            dropped = data['data']['User']['stats']['mangaStatusDistribution'][3]['amount']

            try:
                manga_mean_score = data['data']['User']['stats']['mangaListScores']['meanScore']
            except TypeError:
                manga_mean_score = '**Ingen**'
            if not manga_mean_score:
                manga_mean_score = '**Ingen**'

            color = data['data']['User']['options']['profileColor']
            colors = {
                'blue': 0x3db4f2,
                'purple': 0xc063ff,
                'pink': 0xFC9DD6,
                'orange': 0xEF881A,
                'red': 0xE13333,
                'green': 0x4CCA51,
                'gray': 0x677B94
            }
            if color in colors:
                color = colors[color]
            else:
                color = 0x3db4f2

            embed = discord.Embed(title=user_name, color=color, url=user_url)
            embed.set_author(name='Anilist', icon_url='https://avatars3.githubusercontent.com/u/18018524?s=200&v=4')
            embed.set_thumbnail(url=profile_pic)
            embed.add_field(name='Gj.snittlig vurdering', value=manga_mean_score)
            embed.add_field(name='Antall kapitler lest', value=chapters_read)
            embed.add_field(name='Antall manga lest', value=completed)
            embed.add_field(name='Leser nå', value=reading)
            embed.add_field(name='Planlegger å lese', value=planning)
            embed.add_field(name='Droppet', value=dropped)
            embed.set_footer(text=f'(Norske tider) Oppdatert: {last_updated} | Tid nå: {now}')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Anime(bot))