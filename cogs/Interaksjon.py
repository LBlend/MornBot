import discord
import asyncio
from discord.ext import commands

import requests

class Interaksjon:
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["pat"])
    async def klapp(self, ctx, bruker: discord.Member):
        """Klapp en bruker"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            embed = discord.Embed(description="Jeg vet du er ensom, men du kan ikke klappe deg selv")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/pat").json()
        patGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{ctx.message.author.mention} klappet {bruker.mention}"
        embed.set_image(url=patGif)
        await statusmsg.edit(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["hug"])
    async def klem(self, ctx, bruker: discord.Member):
        """Gi en bruker en klem"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            embed = discord.Embed(description="Jeg vet du er ensom, men du kan ikke klemme deg selv")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/hug").json()
        hugGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{ctx.message.author.mention} ga {bruker.mention} en klem"
        embed.set_image(url=hugGif)
        await statusmsg.edit(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["cuddle"])
    async def kos(self, ctx, bruker: discord.Member):
        """Kos med en bruker"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            embed = discord.Embed(description="Jeg vet du er ensom, men du kan ikke kose med deg selv")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/cuddle").json()
        cuddleGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{ctx.message.author.mention} ga {bruker.mention} en klem"
        embed.set_image(url=cuddleGif)
        await statusmsg.edit(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def poke(self, ctx, bruker: discord.Member):
        """Poke en bruker"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            embed = discord.Embed(description="Jeg vet du er ensom, men du kan ikke poke deg selv")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/poke").json()
        pokeGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{ctx.message.author.mention} poket {bruker.mention}"
        embed.set_image(url=pokeGif)
        await statusmsg.edit(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["kiss"])
    async def kyss(self, ctx, bruker: discord.Member):
        """Kyss en bruker"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            embed = discord.Embed(description="Jeg vet du er ensom, men du kan ikke kysse deg selv")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/kiss").json()
        kissGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{ctx.message.author.mention} kysset {bruker.mention}"
        embed.set_image(url=kissGif)
        await statusmsg.edit(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["tickle"])
    async def kil(self, ctx, bruker: discord.Member):
        """Kil en bruker"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            embed = discord.Embed(description="Jeg vet du er ensom, men du kan ikke kile deg selv")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/tickle").json()
        tickleGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{ctx.message.author.mention} kilte {bruker.mention}"
        embed.set_image(url=tickleGif)
        await statusmsg.edit(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["dum", "idiot"])
    async def baka(self, ctx, bruker: discord.Member):
        """Bruk når folk er dumme"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            embed = discord.Embed(description="Jeg vet du har lav selvtillit, men du kan ikke kalle deg selv en BAKA")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/baka").json()
        bakaGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{bruker.mention} er en BAKA"
        embed.set_image(url=bakaGif)
        await statusmsg.edit(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["spank"])
    async def pisk(self, ctx, *bruker: discord.Member):
        """Pisk en bruker (NSFW)"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk NSFW
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(color=0xFF0000, description=":x: Du må være i en NSFW-kanal")
            await statusmsg.edit(embed=embed)
            return

        if not bruker:
            bruker = ctx.message.author

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/spank").json()
        spankGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{ctx.message.author.mention} pisket {bruker.mention}"
        embed.set_image(url=spankGif)
        await statusmsg.edit(embed=embed)

    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["slå", "klask"])
    async def slap(self, ctx, bruker: discord.Member):
        """Slå noen"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            embed = discord.Embed(description="Vi er imot selvskading. Ikke klask deg selv")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/slap").json()
        slapGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"{ctx.message.author.mention} klasket {bruker.mention}"
        embed.set_image(url=slapGif)
        await statusmsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Interaksjon(bot))