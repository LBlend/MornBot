import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from time import time
import platform
from os import getpid
from psutil import Process
from math import ceil
from operator import itemgetter

from .utils import Defaults

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']
    website = config['website']
    github = config['github']


class Info(commands.Cog):
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
            value=f'{platform.version()}\n' +
            f'{platform.system()} {platform.release()}')
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
                  f'| [Nettside]({website}) | [Github]({github})')
        embed.set_footer(
            text=dev.name, icon_url=dev.avatar_url)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True, external_emojis=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['serverinfo', 'si', 'gi'])
    async def guildinfo(self, ctx):
        """Viser info om guilden"""

        guild_created_date = ctx.guild.created_at.strftime('%d %b %Y %H:%M')
        since_created_days = (
                ctx.message.created_at - ctx.guild.created_at).days

        if since_created_days is 1:
            since_created_days_string = 'dag'
        else:
            since_created_days_string = 'dager'

        total_members = 0
        bot_members = 0
        online_members = 0
        idle_members = 0
        dnd_members = 0
        offline_members = 0
        for member in ctx.guild.members:
            total_members += 1
            if member.bot:
                bot_members += 1
            if str(member.status) == 'online':
                online_members += 1
            elif str(member.status) == 'idle':
                idle_members += 1
            elif str(member.status) == 'dnd':
                dnd_members += 1
            elif str(member.status) == 'offline':
                offline_members += 1

        roles = []
        for role in ctx.guild.roles:
            if role.name != '@everyone':
                roles.append(role.name)
        if roles is []:
            roles = ['**Ingen Roller**']
        roles.reverse()
        roles = ', '.join(roles)
        if len(roles) > 1024:
            roles = f'Skriv `{prefix}{ctx.command}` for å se rollene'

        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        total_channels = text_channels + voice_channels

        flags = {
            'us': ':flag_us:',
            'eu': ':flag_eu:',
            'singapore': ':flag_sg:',
            'london': ':flag_gb:',
            'sydeny': ':flag_au:',
            'amsterdam': ':flag_nl:',
            'frankfurt': ':flag_de:',
            'brazil': ':flag_br:',
            'japan': ':flag_jp:',
            'russia': ':flag_ru:',
            'southafrica': ':flag_za:',
            'hongkong': ':flag_hk:'
            }
        region = str(ctx.guild.region)
        if region.startswith('us'):
            region = 'us'
        elif region.startswith('eu'):
            region = 'eu'
        elif region.startswith('amsterdam'):
            region = 'amsterdam'
        flag = flags[region]

        embed = discord.Embed(color=0x0085ff)
        embed.set_author(name=ctx.guild.name)
        embed.set_thumbnail(url=ctx.guild.icon_url_as(format='png'))
        embed.add_field(name='ID', value=ctx.guild.id)
        embed.add_field(name='Eier', value=ctx.guild.owner.mention)
        embed.add_field(name='Region', value=f'{flag} {ctx.guild.region}')
        embed.add_field(
            name='Server lagd',
            value=f'{guild_created_date}\n{since_created_days} ' +
            f'{since_created_days_string} siden')
        embed.add_field(
            name=f'Kanaler ({total_channels})',
            value=f'Kategorier: **{categories}\n' +
                  f'**Tekst: **{text_channels}**\nTale: **{voice_channels}**')
        embed.add_field(
            name=f'Medlemmer ({total_members})',
            value=f'Mennesker: **{int(total_members) - int(bot_members)}**\n' +
                  f'Båtter: **{bot_members}**\n' +
                  f'<:online:516328785910431754>{online_members} ' +
                  f'<:idle:516328783347843082>{idle_members} ' +
                  f'<:dnd:516328782844395579>{dnd_members} ' +
                  f'<:offline:516328785407246356>{offline_members}')
        embed.add_field(
            name=f'Roller ({len(ctx.guild.roles) - 1})', value=roles,
            inline=False)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['serverroller'])
    async def guildroller(self, ctx):
        """Viser rollene i en guild"""

        roles = []
        for role in ctx.guild.roles:
            if role.name != '@everyone':
                roles.append(role.name)
        if roles is []:
            roles = ['**Ingen Roller**']
        roles.reverse()
        roles = ', '.join(roles)

        embed = discord.Embed(
            color=0x0085ff, description=roles)
        embed.set_author(
            name=f'Roller ({len(ctx.guild.roles) - 1}): {ctx.guild.name}')
        embed.set_thumbnail(url=ctx.guild.icon_url_as(format='png'))
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True, external_emojis=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['userinfo', 'ui', 'bi'])
    async def brukerinfo(self, ctx, *, bruker: discord.Member=None):
        """Viser info om en bruker"""

        if not bruker:
            bruker = ctx.author

        join_index = sorted(
            ctx.guild.members, key=lambda m: m.joined_at).index(bruker) + 1
        creation_index = sorted(
            ctx.guild.members, key=lambda m: m.created_at).index(bruker) + 1

        bruker_joined_date = bruker.joined_at.strftime('%d %b %Y %H:%M')
        bruker_created_date = bruker.created_at.strftime('%d %b %Y %H:%M')
        since_joined_days = (ctx.message.created_at - bruker.joined_at).days
        since_created_days = (ctx.message.created_at - bruker.created_at).days
        if since_created_days is 1:
            since_created_days_string = 'dag'
        else:
            since_created_days_string = 'dager'
        if since_joined_days is 1:
            since_joined_days_string = 'dag'
        else:
            since_joined_days_string = 'dager'

        roles = []
        for role in bruker.roles:
            if role.name != '@everyone':
                roles.append(role.name)
        if not roles:
            roles = ['**Ingen Roller**']
        roles.reverse()
        roles = ', '.join(roles)

        if len(roles) > 1024:
            roles = f'Skriv `{prefix}{ctx.command}` for å se rollene'

        if str(bruker.color) != '#000000':
            color = bruker.color
        else:
            color = discord.Colour(0x99AAB5)

        statuses = {
            'online': '<:online:516328785910431754> Pålogget',
            'idle': '<:idle:516328783347843082> Inaktiv',
            'dnd': '<:dnd:516328782844395579> Ikke forstyrr',
            'offline': '<:offline:516328785407246356> Frakoblet'
        }
        status = statuses[str(bruker.status)]

        embed = discord.Embed(
            color=color,
            description=f'{bruker.mention}\nID: {bruker.id}\n{status}')
        if bruker.display_name == bruker.name:
            embed.set_author(
                name=f'{bruker.name}#{bruker.discriminator}',
                icon_url=bruker.avatar_url)
        else:
            embed.set_author(
                name=f'{bruker.name}#{bruker.discriminator} | ' +
                f'{bruker.display_name}', icon_url=bruker.avatar_url)
        embed.set_thumbnail(url=bruker.avatar_url_as(static_format='png'))
        embed.add_field(
            name='Bruker lagd',
            value=f'{bruker_created_date}\n{since_created_days_string} ' +
            f'{since_created_days_string} siden')
        embed.add_field(
            name='Ble med i serveren',
            value=f'{bruker_joined_date}\n{since_joined_days} ' +
            f'{since_joined_days_string} siden')
        embed.add_field(name='Roller', value=roles, inline=False)
        embed.set_footer(
            text=f'#{join_index} Medlem av serveren | ' +
            f'#{creation_index} Eldste brukeren på serveren')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def brukerroller(self, ctx, bruker: discord.Member=None):
        """Viser rollene til en bruker"""

        if not bruker:
            bruker = ctx.author

        roles = []
        for role in bruker.roles:
            if role.name != '@everyone':
                roles.append(role.name)
        if roles is []:
            roles = ['**Ingen Roller**']
        roles.reverse()
        roles = ', '.join(roles)

        if str(bruker.color) != '#000000':
            color = bruker.color
        else:
            color = discord.Colour(0x99AAB5)

        embed = discord.Embed(
            color=color, description=roles)
        if bruker.display_name == bruker.name:
            embed.set_author(
                name=f'Roller: {bruker.name}#{bruker.discriminator}',
                icon_url=bruker.avatar_url_as(static_format='png'))
        else:
            embed.set_author(
                name=f'Roller: {bruker.name}#{bruker.discriminator} | ' +
                f'{bruker.display_name}', icon_url=bruker.avatar_url)
        embed.set_thumbnail(url=bruker.avatar_url)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(alises=['roleinfo'])
    async def rolleinfo(self, ctx, *, rolle: discord.Role):
        """Viser info om en rolle"""

        if rolle.name == '@everyone':
            return await Defaults.error_fatal_send(
                ctx,
                text='Skriv inn en annen rolle enn @everyone', mention=False)

        if str(rolle.color) != '#000000':
            color = rolle.color
        else:
            color = discord.Colour(0x99AAB5)

        if rolle.mentionable:
            mentionable = 'Ja'
        else:
            mentionable = 'Nei'

        if rolle.hoist:
            hoisted = 'Ja'
        else:
            hoisted = 'Nei'

        rolle_created_date = rolle.created_at.strftime('%d %b %Y %H:%M')
        since_created_days = (ctx.message.created_at - rolle.created_at).days

        if since_created_days is 1:
            since_created_days_string = 'dag'
        else:
            since_created_days_string = 'dager'

        members = []
        for member in rolle.members:
            members.append(member.mention)
        if members is []:
            members = ['**Ingen Medlemmer**']
        members = ' '.join(members)

        if len(members) > 1024:
            members = 'For mange medlemmer for å vise her'

        embed = discord.Embed(
            description=f'{rolle.mention}\n**ID:** {rolle.id}', color=color)
        embed.add_field(name='Antall med rollen', value=len(rolle.members))
        embed.add_field(name='Fargekode', value=str(rolle.color))
        embed.add_field(
            name='Laget den',
            value=f'{rolle_created_date}\n{since_created_days} ' +
            f'{since_created_days_string} siden')
        embed.add_field(name='Posisjon', value=rolle.position)
        embed.add_field(name='Nevnbar', value=mentionable)
        embed.add_field(name='Vises separat i medlemsliste', value=hoisted)
        embed.add_field(
            name='Brukere med rollen', value=members, inline=False)
        embed.set_footer(text=rolle.guild.name, icon_url=rolle.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def avatar(self, ctx, bruker: discord.Member=None):
        """Viser avataren til en bruker"""

        if not bruker:
            bruker = ctx.author

        if str(bruker.color) != '#000000':
            color = bruker.color
        else:
            color = discord.Colour(0x99AAB5)

        embed = discord.Embed(
            color=color,
            description=f'[Link]({bruker.avatar_url_as(static_format="png")})')
        embed.set_image(url=bruker.avatar_url_as(static_format='png'))
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['serverikon', 'servericon', 'guildicon'])
    async def guildikon(self, ctx):
        """Viser ikonet til serveren du er i"""

        embed = discord.Embed(
            color=0x0085ff,
            description=f'[Link]({ctx.guild.icon_url_as(format="png")})')
        embed.set_image(url=ctx.guild.icon_url_as(format='png'))
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['invite'])
    async def inviter(self, ctx):
        """Inviter meg"""

        embed = discord.Embed(color=0x0085ff)
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

        embed = discord.Embed(color=0x0085ff)
        embed.add_field(
            name='Oppetid',
            value=f'{days}d, {hours}t, {minutes}m, {seconds}s')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ping(self, ctx):
        """Sjekk pingen til båtten"""

        embed = discord.Embed(color=0x0085ff)
        embed.add_field(name='Ping', value=f'{int(self.bot.latency * 1000)}ms')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['githubrepo', 'repo', 'git'])
    async def github(self, ctx):
        """Sender link til Github-repoet mitt"""

        embed = discord.Embed(color=0x0085ff)
        embed.set_thumbnail(
            url='https://cdn2.iconfinder.com/data/icons/black-' +
                'white-social-media/64/social_media_logo_github-512.png')
        embed.add_field(
            name='Github Repo',
            value=f'[Klikk her]({github}) ' +
            'for å se den dritt skrevne kildekoden min')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['oldest'])
    async def eldst(self, ctx, *side: int):
        """Liste over de eldste brukerene på serveren"""

        if side is ():
            side = 1
        else:
            side = side[0]

        if side <= 0:
            side = 1

        start_index = (side - 1) * 10
        end_index = side * 10

        formatted_string = ''
        pagecount = ceil(len(ctx.guild.members) / 10)

        if side > pagecount:
            embed = discord.Embed(
                color=0xFF0000,
                description=':x: Ugyldig sidetall')
            return await ctx.send(embed=embed)

        members = sorted(
            ctx.guild.members,
            key=lambda m: m.created_at)[start_index:end_index]
        for member in members:
            bruker = ctx.guild.get_member(member.id)
            bruker_created_date = bruker.created_at.strftime('%d %b %Y %H:%M')
            bruker_index = (members.index(member) + 1) + start_index
            formatted_string += f'#{bruker_index} {bruker.mention} ' +\
                f'- {bruker_created_date}\n'

        embed = discord.Embed(color=0xE67E22)
        embed.add_field(
            name='Eldste Discordbrukerene på serveren', value=formatted_string)
        embed.set_footer(text=f'Side: {side}/{pagecount}')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def joinorder(self, ctx, *side: int):
        """Liste over de første medlemmene av serveren"""

        if side is ():
            side = 1
        else:
            side = side[0]

        if side <= 0:
            side = 1

        start_index = (side - 1) * 10
        end_index = side * 10

        formatted_string = ''
        pagecount = ceil(len(ctx.guild.members) / 10)

        members = sorted(
            ctx.guild.members,
            key=lambda m: m.joined_at)[start_index:end_index]
        for member in members:
            bruker = ctx.guild.get_member(member.id)
            bruker_joined_date = bruker.joined_at.strftime('%d %b %Y %H:%M')
            bruker_index = (members.index(member) + 1) + start_index
            formatted_string += f'#{bruker_index} {bruker.mention} ' +\
                f'- {bruker_joined_date}\n'

        embed = discord.Embed(color=0xE67E22)
        embed.add_field(
            name='Første Discordbrukerene på serveren', value=formatted_string)
        embed.set_footer(text=f'Side: {side}/{pagecount}')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def mestspilt(self, ctx):
        """Sjekk hvilket spill som blir spilt mest på serveren"""

        spill = {}
        for member in ctx.guild.members:
            if member.bot:
                continue
            if member.activity is None:
                continue
            if member.activity.name not in spill:
                spill[member.activity.name] = 1
                continue
            spill[member.activity.name] += 1

        if spill == {}:
            return await ctx.send('Det er ingen som spiller noe akkurat nå')

        gamelist = sorted(spill.items(), key=itemgetter(1), reverse=True)
        formatted_string = ''
        for game in gamelist[0:10]:
            formatted_string += f'**{game[0]}**: {game[1]}\n'

        embed = discord.Embed(
            color=0xE67E22,
            title='De mest spilte spillene på serveren for øyeblikket',
            description=formatted_string)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
