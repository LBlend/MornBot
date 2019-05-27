import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from requests import get

from .utils import Defaults

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    twitch_api_key = config['twitch_api_key']


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['twitchuser', 'twitchstream'])
    async def twitch(self, ctx, bruker):
        """Viser informasjon om en Twitch-bruker"""

        async with ctx.channel.typing():

            user_data = get(
                f'https://api.twitch.tv/kraken/users/{bruker}?' +
                f'client_id={twitch_api_key}').json()
            follow_count_data = get(
                f'https://api.twitch.tv/kraken/channels/{bruker}/follows?' +
                f'client_id={twitch_api_key}').json()
            livestream_data = get(
                f'https://api.twitch.tv/kraken/streams/{bruker}?' +
                f'client_id={twitch_api_key}').json()
            try:
                profile_pic = user_data['logo']
            except KeyError:
                return await Defaults.error_fatal_send(
                    ctx, text='Fant ikke bruker!\n\n' +
                              f'Skriv `{prefix}help {ctx.command}` for hjelp')

            username = user_data['display_name']
            name = user_data['name']
            bio = user_data['bio']
            creation_date = str(user_data['created_at'])
            creation_date_formatted = f'{creation_date[8:10]}.' +\
                f'{creation_date[5:7]}.{creation_date[:4]}'
            user_url = f'https://twitch.tv/{name}'
            follow_count = str(follow_count_data['_total'])

            embed = discord.Embed(title=username, color=0x392E5C, url=user_url)
            embed.set_author(
                name='Twitch',
                icon_url='http://www.gamergiving.org/wp-content/' +
                         'uploads/2016/03/twitch11.png')
            embed.set_thumbnail(url=profile_pic)
            embed.add_field(name='Bio', value=bio, inline=False)
            embed.add_field(name='Følgere', value=str(follow_count))
            embed.add_field(name='Bruker lagd', value=creation_date_formatted)
            await Defaults.set_footer(ctx, embed)

            try:
                livestream_title = livestream_data['stream']\
                    ['channel']['status']
                livestream_game = livestream_data['stream']['game']
                livestream_preview = livestream_data['stream']\
                    ['preview']['large']
                views = str(livestream_data['stream']['viewers'])
            except TypeError:
                return await ctx.send(embed=embed)

            embed.add_field(
                name=':red_circle: Sender direkte nå',
                value=f'**Antall som ser på:**\n{views}\n\n' +
                f'**Tittel:**\n{livestream_title}\n\n' +
                f'**Spill:**\n{livestream_game}',
                inline=False)
            embed.set_image(url=livestream_preview)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Twitch(bot))
