import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from time import time
import platform
from os import getpid
from psutil import Process

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    website = config['website']
    github = config['github']


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True, external_emojis=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['info', 'about', 'om', 'båttinfo'])
    async def botinfo(self, ctx):
        """Viser info om meg"""

        dev = await self.bot.fetch_user(170506717140877312)

        now = time()
        diff = int(now - self.bot.uptime)
        days, remainder = divmod(diff, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        process = Process(getpid())
        memory_usage = round(process.memory_info().rss / 1000000, 1)
        cpu_percent = process.cpu_percent()

        total_members = []
        online_members = []
        idle_members = []
        dnd_members = []
        offline_members = []
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.id in total_members:
                    continue
                total_members.append(member.id)
                if str(member.status) == 'online':
                    online_members.append(member.id)
                elif str(member.status) == 'idle':
                    idle_members.append(member.id)
                elif str(member.status) == 'dnd':
                    dnd_members.append(member.id)
                elif str(member.status) == 'offline':
                    offline_members.append(member.id)

        embed = discord.Embed(color=ctx.me.color, url=website)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name='Dev',
            value=f'{dev.mention}\n{dev.name}#{dev.discriminator}')
        embed.add_field(
            name='Oppetid', value=f'{days}d {hours}t {minutes}m {seconds}s')
        embed.add_field(
            name='Ping', value=f'{int(self.bot.latency * 1000)}ms')
        embed.add_field(name='Servere', value=len(self.bot.guilds))
        embed.add_field(name='Discord.py Versjon', value=discord.__version__)
        embed.add_field(name='Python Versjon', value=platform.python_version())
        embed.add_field(
            name='Ressursbruk',
            value=f'RAM: {memory_usage} MiB\nCPU: {cpu_percent}%')
        embed.add_field(
            name='Maskin',
            value=f'{platform.system()} {platform.release()}')
        embed.add_field(
            name=f'Brukere ({len(total_members)})',
            value=f'<:online:516328785910431754>{len(online_members)} ' +
                  f'<:idle:516328783347843082>{len(idle_members)} ' +
                  f'<:dnd:516328782844395579>{len(dnd_members)} ' +
                  f'<:offline:516328785407246356>{len(offline_members)}')
        embed.add_field(
            name='Lenker',
            value='[Inviter](https://discordapp.com/oauth2/authorize?client_' +
                  f'id={self.bot.user.id}&permissions=388174&scope=bot) ' +
                  f'| [Nettside]({website}) | [Kildekode]({github})')
        embed.set_footer(
            text=dev.name, icon_url=dev.avatar_url)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['invite'])
    async def inviter(self, ctx):
        """Inviter meg"""

        embed = discord.Embed(color=ctx.me.color)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name='Invitasjonslink',
            value='[Klikk her](https://discordapp.com/oauth2/authorize?clien' +
                  f't_id={self.bot.user.id}&permissions=388174&scope=bot) ' +
                  'for å invitere meg til serveren din')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['uptime'])
    async def oppetid(self, ctx):
        """Sjekk hvor lenge båtten har kjørt"""

        now = time()
        diff = int(now - self.bot.uptime)
        days, remainder = divmod(diff, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(color=ctx.me.color)
        embed.add_field(
            name='Oppetid',
            value=f'{days}d, {hours}t, {minutes}m, {seconds}s')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ping(self, ctx):
        """Sjekk pingen til båtten"""

        embed = discord.Embed(color=ctx.me.color)
        embed.add_field(name='Ping', value=f'{int(self.bot.latency * 1000)}ms')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['githubrepo', 'repo', 'git'])
    async def github(self, ctx):
        """Sender link til Github-repoet mitt"""

        embed = discord.Embed(color=ctx.me.color)
        embed.set_thumbnail(
            url='https://cdn2.iconfinder.com/data/icons/black-' +
                'white-social-media/64/social_media_logo_github-512.png')
        embed.add_field(
            name='Github Repo',
            value=f'[Klikk her]({github}) ' +
            'for å se den dritt skrevne kildekoden min')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))