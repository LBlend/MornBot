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

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk NSFW
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(color=0xFF0000, description=":x: Du må være i en NSFW-kanal")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/hololewd").json()
        hololewd = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=hololewd)
        await statusmsg.edit(embed=embed)


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def holoero(self, ctx):
        """Sender et erotisk bilde av Holo"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk NSFW
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(color=0xFF0000, description=":x: Du må være i en NSFW-kanal")
            await statusmsg.edit(embed=embed)
            return

        #   Hent data
        data = requests.get("https://nekos.life/api/v2/img/holoero").json()
        holoero = data["url"]

        #   Embed
        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=holoero)
        await statusmsg.edit(embed=embed)

def setup(bot):
    bot.add_cog(NSFW(bot))