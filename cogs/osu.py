import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from requests import get
import urllib.parse

from .utils import Defaults


with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    osu_api_key = config['osu_api_key']

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

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if gamemode in gamemodes:
            gamemode = gamemodes[gamemode]
        else:
            gamemode = '0'

        osu_user = bruker

        try:
            url = 'https://osu.ppy.sh/api/get_user?' + \
                  urllib.parse.urlencode({
                      'u': osu_user,
                      'm': gamemode,
                      'k': osu_api_key})
            data = get(url).json()

            osu_user_id = data[0]['user_id']

        except IndexError:
            return await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Fant ikke bruker!\n\n' +
                     f'Skriv `{prefix}help {ctx.command}` for hjelp',
                mention=False)

        user_url = f'https://osu.ppy.sh/users/{osu_user_id}'
        profile_pic = f'http://a.ppy.sh/{osu_user_id}'
        username = data[0]['username']
        rank = data[0]['pp_rank']

        if rank == '#0':
            return await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Brukeren har ikke spilt nok!', mention=False)

        level = str(round(float(data[0]['level']), 2))
        country_rank = data[0]['pp_country_rank']
        country = data[0]['country']
        pp = round(float(data[0]['pp_raw']))
        acc = round(float(data[0]['accuracy']), 2)
        ss_ranks = data[0]['count_rank_ss']
        ssh_ranks = data[0]['count_rank_ssh']
        s_ranks = data[0]['count_rank_s']
        sh_ranks = data[0]['count_rank_sh']
        a_ranks = data[0]['count_rank_a']
        playcount = data[0]['playcount']
        join_date = data[0]['join_date']
        hours_played = round((int(data[0]['total_seconds_played']) / 60) / 60)

        embed = discord.Embed(
            title=username, color=0xCC5288, url=user_url,
            description=f'<:ScoreSSPlus:476372071014727706>{ssh_ranks} ' +
            f'<:ScoreSS:476372071316848640>{ss_ranks} ' +
            f'<:ScoreSPlus:476372071342145536>{sh_ranks} ' +
            f'<:ScoreS:476372070989692929>{s_ranks} ' +
            f'<:ScoreA:476372070976978955>{a_ranks}')
        embed.set_author(
            name='osu!',
            icon_url='https://upload.wikimedia.org/wikipedia/commons/' +
                     'd/d3/Osu%21Logo_%282015%29.png')
        embed.set_thumbnail(url=profile_pic)
        embed.add_field(name='Global Ranking', value=f'#{rank}')
        embed.add_field(
            name='Country Ranking',
            value=f':flag_{country.lower()}:#{country_rank}')
        embed.add_field(name='PP', value=pp)
        embed.add_field(name='Accuracy', value=f'{acc}%')
        embed.add_field(name='Level', value=level)
        embed.add_field(name='Play Count', value=playcount)

        #   Ja, dette er ekte. Ikke klag, det funker
        embed.set_footer(
            text='Joined: ' +
                 f'{join_date[8:10]}.{join_date[5:7]}.{join_date[:4]} ' +
                 f'{join_date[11:]} | Hours played: {hours_played}')
        await status_msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
