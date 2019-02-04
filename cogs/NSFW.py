import discord
import asyncio
from discord.ext import commands

import requests

class NSFW:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def hololewd(self, ctx):
        """Sender et lewd bilde av Holo"""

        #   Sjekk NSFW
        if not ctx.channel.is_nsfw():
            await ctx.send("Funker bare i NSFW-kanaler")
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/hololewd").json()
        hololewd = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=hololewd)
        await ctx.send(embed=embed)


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def holoero(self, ctx):
        """Sender et erotisk bilde av Holo"""

        #   Sjekk NSFW
        if not ctx.channel.is_nsfw():
            await ctx.send("Funker bare i NSFW-kanaler")
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/holoero").json()
        holoero = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=holoero)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(NSFW(bot))