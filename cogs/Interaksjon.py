import discord
import asyncio
from discord.ext import commands

import requests

class Interaksjon:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["pat"])
    async def klapp(self, ctx, bruker: discord.Member):
        """Klapp en bruker"""

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            await ctx.send("Jeg vet du er ensom, men du kan ikke klapppe deg selv")
            return

        #   Hent data
        apiUrl = "https://nekos.life/api/v2/img/pat"
        data = requests.get(apiUrl).json()
        patGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"<@{ctx.message.author.id}> klappet <@{bruker.id}>"
        embed.set_image(url=patGif)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(aliases=["hug"])
    async def klem(self, ctx, bruker: discord.Member):
        """Gi en bruker en klem"""

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            await ctx.send("Jeg vet du er ensom, men du kan ikke klemme deg selv")
            return

        #   Hent data
        apiUrl = "https://nekos.life/api/v2/img/hug"
        data = requests.get(apiUrl).json()
        hugGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"<@{ctx.message.author.id}> ga <@{bruker.id}> en klem"
        embed.set_image(url=hugGif)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(aliases=["cuddle"])
    async def kos(self, ctx, bruker: discord.Member):
        """Kos med en bruker"""

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            await ctx.send("Jeg vet du er ensom, men du kan ikke kose med deg selv")
            return

        #   Hent data
        apiUrl = "https://nekos.life/api/v2/img/cuddle"
        data = requests.get(apiUrl).json()
        cuddleGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"<@{ctx.message.author.id}> ga <@{bruker.id}> en klem"
        embed.set_image(url=cuddleGif)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def poke(self, ctx, bruker: discord.Member):
        """Poke en bruker"""

        #   Sett bruker til forfatter om ikke arg blir gitt
        if bruker.id == ctx.message.author.id:
            await ctx.send("Jeg vet du er ensom, men du kan ikke poke deg selv")
            return

        #   Hent data
        apiUrl = "https://nekos.life/api/v2/img/poke"
        data = requests.get(apiUrl).json()
        pokeGif = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.description = f"<@{ctx.message.author.id}> poket <@{bruker.id}>"
        embed.set_image(url=pokeGif)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Interaksjon(bot))