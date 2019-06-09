import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

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

        total_members = ctx.guild.member_count
        bot_members = 0
        online_members = 0
        idle_members = 0
        dnd_members = 0
        offline_members = 0
        for member in ctx.guild.members:
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
            roles = f'Skriv `{prefix}guildroller` for å se rollene'
        if roles == '':
            roles = '**Ingen roller**'

        boosters = []
        premium_subscribers = sorted(
            ctx.guild.premium_subscribers, key=lambda m: m.premium_since)
        for booster in premium_subscribers:
            boosters.append(booster.mention)
        if boosters is []:
            boosters = ['**Ingen boosters**']
        boosters = ' '.join(boosters)
        if len(boosters) > 1024:
            boosters = f'Skriv `{prefix}boosters` for å se boosters'
        if boosters == '':
            boosters == '**Ingen boosters**'
        

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
            'hongkong': ':flag_hk:',
            'india': ':flag_in:'
            }
        region = str(ctx.guild.region)
        if region.startswith('us'):
            region = 'us'
        elif region.startswith('eu'):
            region = 'eu'
        elif region.startswith('amsterdam'):
            region = 'amsterdam'
        try:
            flag = flags[region]
        except KeyError:
            flag = ':question:'

        region_names = {
            'eu-central': 'Sentral-Europa',
            'eu-west': 'Vest-Europa',
            'hongkong': 'Hong Kong',
            'russia': 'Russland',
            'southafrica': 'Sør-Afrika',
            'us-central': 'Midt-USA',
            'us-east': 'New Jersey',
            'us-south': 'Sør-USA',
            'us-west': 'California',
            'vip-amsterdam': 'Amsterdam (VIP)',
            'vip-us-east': 'Øst-USA (VIP)',
            'vip-us-west': 'Vest-USA (VIP)',
        }
        try:
            region_name = region_names[str(ctx.guild.region)]
        except KeyError:
            region_name = str(ctx.guild.region).title()

        features_string = ''
        if ctx.guild.features != []:
            features = {
                'VIP_REGIONS': 'VIP',
                'VANITY_URL': 'Egen URL',
                'INVITE_SPLASH': 'Invitasjonsbilde',
                'VERIFIED': 'Verifisert',
                'PARTNERED': 'Discord Partner',
                'MORE_EMOJI': 'Ekstra emoji',
                'DISCOVERABLE': '',
                'COMMERCE': 'Butikkanaler',
                'LURKABLE': 'Kan ses uten join',
                'NEWS': 'Nyhetskanaler',
                'BANNER': 'Banner',
                'ANIMATED_ICON': 'Animert ikon',
            }
            for feature in ctx.guild.features:
                features_string += f'{features[feature]}\n'

        photos = {}
        if ctx.guild.splash_url:
            photos['Invitasjonsbilde'] = ctx.guild.splash_url_as(format='png')
        if ctx.guild.banner_url:
            photos['Banner'] = ctx.guild.banner_url_as(format='png')

        verification_level = {
            'none': 'ingen',
            'low': 'e-post',
            'medium': 'e-post, registrert i 5 min',
            'high': 'e-post, registrert i 5 min, medlem i 10 min',
            'extreme': 'telefon'
        }
        verification = verification_level[str(ctx.guild.verification_level)]

        content_filter = {
            'disabled': 'nei',
            'no_role': 'for alle uten rolle',
            'all_members': 'ja'
        }
        content = content_filter[str(ctx.guild.explicit_content_filter)]

        embed = discord.Embed(
            color=ctx.me.color,
            description=f'**Verifiseringskrav:** {verification}\n' +
                        f'**Innholdsfilter:** {content}\n' +
                        f'**Boost Tier:** {ctx.guild.premium_tier}')
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format='png'))
        embed.add_field(name='ID', value=ctx.guild.id)
        embed.add_field(name='Eier', value=ctx.guild.owner.mention)
        embed.add_field(name='Region', value=f'{flag} {region_name}')
        embed.add_field(
            name='Server lagd',
            value=f'{guild_created_date}\n{since_created_days} ' +
            f'{since_created_days_string} siden')
        embed.add_field(
            name=f'Kanaler ({total_channels})',
            value=f'Tekst: **{text_channels}**\n' +
            f'Tale: **{voice_channels}**\n' +
            f'Kategorier: **{categories}**')
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
        if ctx.guild.premium_tier is not 0:
            embed.add_field(
                name=f'Boosters ({ctx.guild.premium_subscription_count})',
                value=boosters, inline=False)

        if features_string != '':
            embed.add_field(name='Tillegsfunksjoner', value=features_string)

        if photos != {}:
            photos_string = ''
            for key, value in photos.items():
                photos_string += f'[{key}]({value})\n'
            embed.add_field(name='Bilder', value=photos_string)
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

        if roles == '':
            roles = '**Ingen roller**'

        embed = discord.Embed(
            color=ctx.me.color, description=roles)
        embed.set_author(
            name=f'Roller ({len(ctx.guild.roles) - 1}): {ctx.guild.name}')
        embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format='png'))
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['guildboosters', 'serverboosters'])
    async def boosters(self, ctx):
        """Viser boosters i en guild"""

        boosters = []
        premium_subscribers = sorted(
            ctx.guild.premium_subscribers, key=lambda m: m.premium_since)
        for booster in premium_subscribers:
            boosters.append(booster.mention)
        if boosters is []:
            boosters = ['**Ingen boosters**']
        boosters = ' '.join(boosters)
        if boosters == '':
            boosters == '**Ingen boosters**'

        embed = discord.Embed(
            color=ctx.me.color, description=boosters)
        embed.set_author(
            name='Boosters ' +
            f'({ctx.guild.premium_subscription_count}): {ctx.guild.name}')
        embed.set_thumbnail(url=ctx.guild.icon_url_as(static_format='png'))
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['serverikon', 'servericon', 'guildicon'])
    async def guildikon(self, ctx):
        """Viser ikonet til serveren du er i"""

        embed = discord.Embed(
            color=ctx.me.color,
            description=f'[Link]({ctx.guild.icon_url_as(static_format="png")})')
        embed.set_image(url=ctx.guild.icon_url_as(static_format='png'))
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def guildsplash(self, ctx):
        """Viser invite splash til serveren"""

        if not ctx.guild.splash_url:
            return await Defaults.error_warning_send(
                ctx, text='Serveren har ikke en invite splash', mention=False)

        url = ctx.guild.splash_url_as(format='png')

        embed = discord.Embed(
            color=ctx.me.color, description=f'[Link]({url})')
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def guildbanner(self, ctx):
        """Viser invite splash til serveren"""

        if not ctx.guild.banner_url:
            return await Defaults.error_warning_send(
                ctx, text='Serveren har ikke et banner', mention=False)

        url = ctx.guild.banner_url_as(format='png')

        embed = discord.Embed(
            color=ctx.me.color, description=f'[Link]({url})')
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True, external_emojis=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['userinfo', 'ui', 'bi'])
    async def brukerinfo(self, ctx, *, bruker: discord.Member=None):
        """Viser info om en bruker"""

        if not bruker:
            bruker = ctx.author

        app = ''
        if str(bruker.mobile_status) != 'offline':
            app += '📱 '
        if str(bruker.web_status) != 'offline':
            app += '🌐 '
        if str(bruker.desktop_status) != 'offline':
            app += '💻'

        join_index = sorted(
            ctx.guild.members, key=lambda m: m.joined_at).index(bruker) + 1
        creation_index = sorted(
            ctx.guild.members, key=lambda m: m.created_at).index(bruker) + 1
        premium_index = sorted(
            ctx.guild.premium_subscribers, key=lambda m: m.premium_since).index(bruker) + 1

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

        if bruker.premium_since:
            premium_since = bruker.premium_since.strftime('%d %b %Y %H:%M')
            premium_since_days = (ctx.message.created_at - bruker.premium_since).days
            if since_joined_days is 1:
                premium_since_days_string = 'dag'
            else:
                premium_since_days_string = 'dager'

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
        if roles == '':
            roles = '**Ingen roller**'

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
            description=f'{bruker.mention}\nID: {bruker.id}\n{status}\n{app}')
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
            value=f'{bruker_created_date}\n{since_created_days} ' +
            f'{since_created_days_string} siden')
        embed.add_field(
            name='Ble med i serveren',
            value=f'{bruker_joined_date}\n{since_joined_days} ' +
            f'{since_joined_days_string} siden')
        if bruker.premium_since:
            embed.add_field(
                name='Boost',
                value=f'{premium_since}\n{premium_since_days} ' +
                f'{premium_since_days_string} siden\n' +
                f'Booster #{premium_index} av serveren',
                inline=False)
        embed.add_field(name=f'Roller ({len(bruker.roles) - 1})',
                        value=roles, inline=False)
        embed.set_footer(
            text=f'#{join_index} Medlem av serveren | ' +
            f'#{creation_index} Eldste brukeren på serveren')

        if bruker.activities:
            games = ''
            for activity in bruker.activities:
                games += f"{activity.name}\n"
            embed.add_field(name='Spiller', value=games, inline=False)
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

        if roles == '':
            roles = '**Ingen roller**'

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
    @commands.guild_only()
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
        if len(members) == 0:
            members = '**Ingen**'

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
            name=f'Brukere med rollen ({len(rolle.members)})',
            value=members, inline=False)
        embed.set_footer(text=rolle.guild.name, icon_url=rolle.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['tekstkanal', 'kanal'])
    async def kanalinfo(self, ctx, *, kanal: discord.TextChannel):
        """Viser info om en tekstkanal"""

        nsfw = 'Nei'
        if kanal.is_nsfw():
            nsfw = 'Ja'

        if kanal.slowmode_delay == 0:
            saktemodus = 'Nei'
        else:
            saktemodus = f'Ja ({kanal.slowmode_delay} sekunder)'

        description = '**Ingen**'
        if kanal.topic:
         description = kanal.topic

        members = []
        for member in kanal.members:
            members.append(member.mention)
        members = ' '.join(members)
        if len(members) > 1024:
            members = 'For mange for å vise her'

        embed = discord.Embed(
            color=ctx.me.color, description=f'{kanal.mention}\nID: {kanal.id}')
        embed.set_author(name=kanal.name, icon_url=kanal.guild.icon_url)
        embed.add_field(name='Beskrivelse', value=description, inline=False)
        embed.add_field(
            name='Laget', value=kanal.created_at.strftime('%d %b %Y %H:%M'))
        embed.add_field(name='NSFW', value=nsfw)
        embed.add_field(name='Saktemodus', value=saktemodus)
        if kanal.category:
            embed.add_field(name='Kategori', value=kanal.category.name)
        embed.add_field(
            name=f'Antall med tilgang ({len(kanal.members)})', value=members)
        embed.set_footer(text=kanal.guild.name, icon_url=kanal.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['talekanalinfo', 'voicechannel'])
    async def talekanal(self, ctx, *, kanal: discord.VoiceChannel):
        """Viser info om en talekanal"""

        if kanal.user_limit == 0:
            limit = '∞ personer'
        else:
            limit = f'{kanal.user_limit} personer'

        embed = discord.Embed(
            color=ctx.me.color, description=f'ID: {kanal.id}')
        embed.set_author(name=kanal.name, icon_url=kanal.guild.icon_url)
        embed.add_field(
            name='Laget', value=kanal.created_at.strftime('%d %b %Y %H:%M'))
        embed.add_field(
            name='Bitrate', value=f'{int(kanal.bitrate / 1000)}kbps')
        embed.add_field(name='Maksgrense', value=limit)
        if kanal.category:
            embed.add_field(name='Kategori', value=kanal.category.name)
        embed.add_field(name=f'Antall koblet til', value=len(kanal.members))
        embed.set_footer(text=kanal.guild.name, icon_url=kanal.guild.icon_url)
        await ctx.send(embed=embed)


    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['emote'])
    async def emoji(self, ctx, emoji: discord.Emoji):
        """Viser info om en CUSTOM emoji som tilhører serveren"""

        animated = 'Nei'
        if emoji.animated:
            animated = 'Ja'

        emoji_2 = await emoji.guild.fetch_emoji(emoji.id)
        try:
            emoji_creator = f'{emoji_2.user.name}#{emoji_2.user.discriminator}'
        except AttributeError:
            emoji_creator = 'Jeg trenger `manage_emojis`-' +\
                            'tillatelsen for å hente dette'

        embed = discord.Embed(
            color=ctx.me.color, description=f'ID: {emoji.id}')
        embed.set_author(name=emoji.name, icon_url=emoji.url)
        embed.add_field(
            name=f'Laget', value=emoji.created_at.strftime('%d %b %Y %H:%M'))
        embed.add_field(name='Animert', value=animated)
        embed.add_field(
            name='Lagt til av',
            value=emoji_creator)
        embed.set_image(url=emoji.url)
        embed.set_footer(text=emoji.guild.name, icon_url=emoji.guild.icon_url)
        await ctx.send(embed=embed)
    

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['serveremoji', 'serveremotes'])
    async def guildemoji(self, ctx):
        """Viser alle emoji som serveren har"""

        embed = discord.Embed(
            title=f"Emoji",
            colour=ctx.me.color)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)

        emoji_string = ''
        for emoji in ctx.guild.emojis:
            if len(emoji_string) > 2000:
                embed.description = emoji_string
                await ctx.send(embed=embed)
                emoji_string = ''
            emoji_string += f'{emoji} '

        embed.description = emoji_string
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
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

        embed = discord.Embed(color=ctx.me.color)
        embed.add_field(
            name='Eldste Discordbrukerene på serveren', value=formatted_string)
        embed.set_footer(text=f'Side: {side}/{pagecount}')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
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

        embed = discord.Embed(color=ctx.me.color)
        embed.add_field(
            name='Første Discordbrukerene på serveren', value=formatted_string)
        embed.set_footer(text=f'Side: {side}/{pagecount}')
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
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
            color=ctx.me.color,
            title='De mest spilte spillene på serveren for øyeblikket',
            description=formatted_string)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def hvemspiller(self, ctx, *, spill: str):
        """Sjekk hvem spiller et spesifisert spik"""

        users = []
        for member in ctx.guild.members:
            if member.bot:
                continue
            if not member.activity:
                continue
            if member.activity.name.lower() == spill.lower():
                spill = member.activity.name
                users.append(f'{member.name}#{member.discriminator}')

        if users == []:
            embed = discord.Embed(
                color=ctx.me.color,
                description='Det er ingen som spiller dette spillet')
            return await ctx.send(embed=embed)

        formatted_string = ''
        for user in users[0:10]:
            formatted_string += f'• {user}\n'

        embed = discord.Embed(
            color=ctx.me.color,
            title=f'Disse spiller {spill} for øyeblikket (maks 10)',
            description=formatted_string)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
