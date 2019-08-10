from discord.ext import commands
import discord

from codecs import open
from json import load as json_load
import locale

from requests import get
import urllib.parse

from cogs.utils import Defaults


with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    osu_api_key = config['osu_api_key']

locale.setlocale(locale.LC_ALL, '')

gamemodes = {
    'taiko': '1',
    'ctb': '2',
    'catch the beat': '2',
    'catch': '2',
    'mania': '3'
}


class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True, external_emojis=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['osustats', 'osuuser', 'osuprofile'])
    async def osuprofil(self, ctx, bruker, gamemode=None):
        """Viser info om en osu! profil"""

        async with ctx.channel.typing():

            if gamemode in gamemodes:
                gamemode = gamemodes[gamemode]
            else:
                gamemode = '0'

            osu_user = bruker

            try:
                url = 'https://osu.ppy.sh/api/get_user?' + urllib.parse.urlencode(
                    {
                        'u': osu_user,
                        'm': gamemode,
                        'k': osu_api_key
                     })
                data = get(url).json()

                osu_user_id = data[0]['user_id']

            except IndexError:
                return await Defaults.error_fatal_send(ctx, text='Fant ikke bruker!\n\n ' +
                                                                 f'Skriv `{prefix}help {ctx.command}` for hjelp')

            user_url = f'https://osu.ppy.sh/users/{osu_user_id}'
            profile_pic = f'http://a.ppy.sh/{osu_user_id}'
            username = data[0]['username']
            rank = int(data[0]['pp_rank'])
            rank = locale.format_string('%d', rank, grouping=True)

            if rank == '#0':
                return await Defaults.error_fatal_send(ctx, text='Brukeren har ikke spilt nok!')

            level = str(round(float(data[0]['level']), 2))
            country_rank = int(data[0]['pp_country_rank'])
            country_rank = locale.format_string('%d', country_rank, grouping=True)
            country = data[0]['country']
            pp = round(float(data[0]['pp_raw']))
            pp = locale.format_string('%d', pp, grouping=True)
            acc = round(float(data[0]['accuracy']), 2)
            ss_ranks = data[0]['count_rank_ss']
            ssh_ranks = data[0]['count_rank_ssh']
            s_ranks = data[0]['count_rank_s']
            sh_ranks = data[0]['count_rank_sh']
            a_ranks = data[0]['count_rank_a']
            playcount = int(data[0]['playcount'])
            playcount = locale.format_string('%d', playcount, grouping=True)
            join_date = data[0]['join_date']
            hours_played = round((int(data[0]['total_seconds_played']) / 60) / 60)

            embed = discord.Embed(title=username, color=0xCC5288, url=user_url,
                                  description=f'<:GradeSSSilver:609830030402387981>{ssh_ranks} ' +
                                              f'<:GradeSS:609830028842237962>{ss_ranks} ' +
                                              f'<:GradeSSilver:609830028913672193>{sh_ranks} ' +
                                              f'<:GradeS:609830028729122843>{s_ranks} ' +
                                              f'<:GradeA:609830029177913344>{a_ranks}')
            embed.set_author(name='osu!', icon_url='https://upload.wikimedia.org/wikipedia/commons/' +
                                                   'd/d3/Osu%21Logo_%282015%29.png')
            embed.set_thumbnail(url=profile_pic)
            embed.add_field(name='Global Ranking', value=rank)
            embed.add_field(name='Country Ranking', value=f':flag_{country.lower()}: {country_rank}')
            embed.add_field(name='PP', value=pp)
            embed.add_field(name='Accuracy', value=f'{acc}%')
            embed.add_field(name='Level', value=level)
            embed.add_field(name='Play Count', value=playcount)

            #   Ja, dette er ekte. Ikke klag, det funker
            embed.set_footer(text=f'Joined: {join_date[8:10]}.{join_date[5:7]}.{join_date[:4]} ' +
                                  f'{join_date[11:]} | Hours played: {hours_played}')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
