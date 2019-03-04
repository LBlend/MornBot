import discord
import asyncio
from discord.ext import commands

import codecs
import json
import datetime
import time
import platform
import os
import psutil

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]

class Info:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["info", "about", "om", "båttinfo"])
    async def botinfo(self, ctx):
        """Viser info om meg"""

        #   Last inn config
        with codecs.open("config.json", "r", encoding="utf8") as f:
            config = json.load(f)
            devId = config["devId"]
            website = config["website"]
            github = config["github"]

        dev = self.bot.get_user(devId)

        #   Uptime
        now = time.time()
        diff = int(now - self.bot.uptime)
        days, remainder = divmod(diff, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        #   Ressursforbruk
        process = psutil.Process(os.getpid())
        mem = round(process.memory_info().rss / 1000000, 1)
        cpuPer = process.cpu_percent()

        #   Medlemstall
        totalmembers = []
        onlinemembers = []
        idlemembers = []
        dndmembers = []
        offlinemembers = []
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.id in totalmembers:
                    pass
                elif str(member.status) == "online":
                    onlinemembers.append(member.id)
                    totalmembers.append(member.id)
                elif str(member.status) == "idle":
                    idlemembers.append(member.id)
                    totalmembers.append(member.id)
                elif str(member.status) == "dnd":
                    dndmembers.append(member.id)
                    totalmembers.append(member.id)
                elif str(member.status) == "offline":
                    offlinemembers.append(member.id)
                    totalmembers.append(member.id)

        #   Embed
        embed = discord.Embed(color=0xE67E22, url=website)
        embed.add_field(name="Dev", value=f"{dev.mention}\n({dev.name}#{dev.discriminator})")
        embed.add_field(name="Oppetid", value=f"{days}d {hours}t {minutes}m {seconds}s")
        embed.add_field(name="Ping", value=f"{int(self.bot.latency * 1000)}ms")
        embed.add_field(name="Servere", value=len(self.bot.guilds))
        embed.add_field(name="Discord.py Versjon", value=discord.__version__)
        embed.add_field(name="Python Versjon", value=platform.python_version())
        embed.add_field(name="Maskin", value=f"{platform.version()[4:11]}\n{platform.system()} {platform.release()}")
        embed.add_field(name="Ressursbruk", value=f"RAM: {mem} MiB\nCPU: {cpuPer}%")
        embed.add_field(name=f"Brukere ({len(totalmembers)})", value=f"<:online:516328785910431754>{len(onlinemembers)} <:idle:516328783347843082>{len(idlemembers)} <:dnd:516328782844395579>{len(dndmembers)} <:offline:516328785407246356>{len(offlinemembers)}")
        embed.add_field(name="Lenker", value=f"[Inviter](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot) | [Nettside]({website}) | [Github]({github})")
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text=f"{dev.name}#{dev.discriminator}", icon_url=dev.avatar_url)
        await ctx.send(embed=embed)


    @commands.guild_only()     
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["serverinfo", "si", "gi"])
    async def guildinfo(self, ctx):
        """Viser info om guilden"""

        guild = ctx.message.guild

        #   Bot join og creation date
        guild_created = guild.created_at.strftime("%d %b %Y %H:%M")
        since_created = (ctx.message.created_at - guild.created_at).days

        #   Medlemstall
        totalmembers = 0
        onlinemembers = 0
        idlemembers = 0
        dndmembers = 0
        offlinemembers = 0
        for member in guild.members:
            if str(member.status) == "online":
                onlinemembers += 1
                totalmembers += 1
            elif str(member.status) == "idle":
                idlemembers += 1
                totalmembers += 1
            elif str(member.status) == "dnd":
                dndmembers += 1
                totalmembers += 1
            elif str(member.status) == "offline":
                offlinemembers += 1
                totalmembers += 1

        #   Roller
        roles = []
        for r in guild.roles:
            if r.name != "@everyone":
                roles.append(r.name)
        if roles == []:
            roles = ["**Ingen Roller**"]
        roles.reverse()
        roles = ", ".join(roles)

        if len(roles) > 1024:
            roles = f"Skriv `{prefix}guildroller` for å se rollene"

        #   Kanaler
        textChannels = len(guild.text_channels)
        voiceChannels = len(guild.voice_channels)
        totalChannels = textChannels + voiceChannels

        #   Regionflagg
        flags = {
            "us": ":flag_us:", 
            "eu": ":flag_eu:", 
            "singapore": ":flag_sg:", 
            "london": ":flag_gb:", 
            "sydeny": ":flag_au:", 
            "amsterdam": ":flag_nl:",
            "frankfurt": ":flag_de:",
            "brazil": ":flag_br:",
            "japan": ":flag_jp:",
            "russia": ":flag_ru:",
            "southafrica": ":flag_za:",
            "hongkong": ":flag_hk:"
            }
        
        region = str(guild.region)

        if region.startswith("us"):
            region = "us"
        elif region.startswith("eu"):
            region = "eu"
        elif region.startswith("amsterdam"):
            region = "amsterdam"

        flag = flags[region]

        #   Embed
        embed = discord.Embed(color=0x0085ff, url=guild.icon_url)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Eier", value=guild.owner.mention)
        embed.add_field(name="Region", value=f"{flag} {guild.region}")
        embed.add_field(name="Server lagd", value=f"{guild_created}\n{since_created} dag(er) siden")
        embed.add_field(name=f"Kanaler ({totalChannels})", value=f"Tekst: {textChannels}\nTale: {voiceChannels}")
        embed.add_field(name=f"Medlemmer ({totalmembers})", value=f"<:online:516328785910431754>Pålogget: **{onlinemembers}**\n<:idle:516328783347843082>Inaktiv: **{idlemembers}**\n<:dnd:516328782844395579>Ikke forstyrr: **{dndmembers}**\n<:offline:516328785407246356>Frakoblet: **{offlinemembers}**")
        embed.add_field(name="Roller", value=roles, inline=False)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name=guild.name)
        await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)     
    @commands.command(aliases=["serverroller"])
    async def guildroller(self, ctx):
        """Viser rollene i en guild"""

        guild = ctx.message.guild

        roles = []
        for r in guild.roles:
            if r.name != "@everyone":
                roles.append(r.name)
        if roles == []:
            roles = ["**Ingen Roller**"]
        roles.reverse()
        roles = ", ".join(roles)

        embed = discord.Embed(color=0x0085ff, url=guild.icon_url, description=roles)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name=f"Roller: {guild.name}")
        await ctx.send(embed=embed)

        
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["userinfo", "ui", "bi"])
    async def brukerinfo(self, ctx, *, bruker: discord.Member=None):
        """Viser info om en bruker"""

        #   Om ingen bruker gitt, sett bruker til author
        if not bruker:
            bruker = ctx.message.author

        guild = ctx.message.guild

        #   Member number
        memberNumber = sorted(guild.members, key=lambda m: m.joined_at).index(bruker) + 1

        #   Join & creation date
        bruker_joined = bruker.joined_at.strftime("%d %b %Y %H:%M")
        bruker_created = bruker.created_at.strftime("%d %b %Y %H:%M")
        since_created = (ctx.message.created_at - bruker.created_at).days
        since_joined = (ctx.message.created_at - bruker.joined_at).days

        #   Roller
        roles = []
        for r in bruker.roles:
            if r.name != "@everyone":
                roles.append(r.name)
        if roles == []:
            roles = ["**Ingen Roller**"]
        roles.reverse()
        roles = ", ".join(roles)

        if len(roles) > 1024:
            roles = f"Skriv `{prefix}brukerroller` for å se rollene"

        #   Farge
        if str(bruker.color) != "#000000":
            color = bruker.color
        else:
            color = discord.Colour(0x99AAB5)

        #   Embed
        embed = discord.Embed(color=color, url=bruker.avatar_url)
        #embed.description = f"{bruker.status}"
        embed.add_field(name="Bruker lagd", value=f"{bruker_created}\n{since_created} dag(er) siden")
        embed.add_field(name="Ble med i serveren", value=f"{bruker_joined}\n{since_joined} dag(er) siden")
        embed.add_field(name="Roller", value=roles, inline=False)
        embed.set_footer(text=f"Bruker #{memberNumber} | ID: {bruker.id}")
        embed.set_thumbnail(url=bruker.avatar_url)

        #   Kallenavn
        if bruker.display_name == bruker.name:
            embed.set_author(name=f"{bruker.name}#{bruker.discriminator}", icon_url=bruker.avatar_url)
        else:
            embed.set_author(name=f"{bruker.name}#{bruker.discriminator} | {bruker.display_name}", icon_url=bruker.avatar_url) 
        
        await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)     
    @commands.command()
    async def brukerroller(self, ctx, bruker: discord.Member=None):
        """Viser rollene til en bruker"""

        if not bruker:
            bruker = ctx.message.author

        roles = []
        for r in bruker.roles:
            if r.name != "@everyone":
                roles.append(r.name)
        if roles == []:
            roles = ["**Ingen Roller**"]
        roles.reverse()
        roles = ", ".join(roles)

        #   Farge
        if str(bruker.color) != "#000000":
            color = bruker.color
        else:
            color = discord.Colour(0x99AAB5)

        embed = discord.Embed(color=color, url=bruker.avatar_url, description=roles)
        embed.set_thumbnail(url=bruker.avatar_url)

        #   Kallenavn
        if bruker.display_name == bruker.name:
            embed.set_author(name=f"Roller: {bruker.name}#{bruker.discriminator}", icon_url=bruker.avatar_url)
        else:
            embed.set_author(name=f"Roller: {bruker.name}#{bruker.discriminator} | {bruker.display_name}", icon_url=bruker.avatar_url)
        
        await ctx.send(embed=embed)


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def avatar(self, ctx, bruker: discord.Member=None):
        """Viser avataren din"""

        if not bruker:
            bruker = ctx.message.author

        if str(bruker.color) != "#000000":
            color = bruker.color
        else:
            color = discord.Colour(0x99AAB5)

        #   Embed
        embed = discord.Embed(color=color, description=f"[Link]({bruker.avatar_url})")
        embed.set_image(url=bruker.avatar_url)
        await ctx.send(embed=embed)

    
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["serverikon", "servericon", "guildicon", "serveravatar", "guildavatar"])
    async def guildikon(self, ctx):
        """Viser ikonet til serveren du er i"""

        #   Embed
        embed = discord.Embed(color=0x0085ff, description=f"[Link]({ctx.message.guild.icon_url})")
        embed.set_image(url=ctx.message.guild.icon_url)
        await ctx.send(embed=embed)


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["invite"])
    async def inviter(self, ctx):
        """Inviter meg"""

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Invitasjonslink", value=f"[Klikk her](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot) for å invitere meg til serveren din")
        await ctx.send(embed=embed)


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["uptime"])
    async def oppetid(self, ctx):
        """Sjekk hvor lenge båtten har kjørt"""

        now = time.time()
        diff = int(now - self.bot.uptime)
        days, remainder = divmod(diff, 24 * 60 * 60)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(color=0x0085ff)
        embed.add_field(name="Oppetid", value=f"{days} dager, {hours} timer, {minutes} minutter, {seconds} sekunder")
        await ctx.send(embed=embed)


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def ping(self, ctx):
        """Sjekk pingen til båtten"""
        embed = discord.Embed(color=0x0085ff)
        embed.add_field(name="Ping", value=f"{int(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed)


    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=["githubrepo", "repo", "git"])
    async def github(self, ctx):
        """Sender link til Github-repoet mitt"""

        #   Hent Github-link
        with codecs.open("config.json", "r", encoding="utf8") as f:
            config = json.load(f)
            github = config["github"]

            #   Embed
            embed = discord.Embed(color=0x0085ff)
            embed.set_thumbnail(url="https://cdn2.iconfinder.com/data/icons/black-white-social-media/64/social_media_logo_github-512.png")
            embed.add_field(name="Github Repo", value=f"[Klikk her]({github}) for å se den dritt skrevne kildekoden min")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))