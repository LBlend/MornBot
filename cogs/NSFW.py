import discord
import asyncio
from discord.ext import commands

import requests

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["bj"])
    async def blowjob(self, ctx):
        """Blowjob"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        if not ctx.channel.is_nsfw():
            embed = discord.Embed(color=0xFF0000, description=":x: Du må være i en NSFW-kanal")
            await statusmsg.edit(embed=embed)
            return

        data = requests.get("https://nekos.life/api/v2/img/bj").json()
        bj = data["url"]

        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=bj)
        await statusmsg.edit(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def yuri(self, ctx):
        """Yuri"""
        
        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        if not ctx.channel.is_nsfw():
            embed = discord.Embed(color=0xFF0000, description=":x: Du må være i en NSFW-kanal")
            await statusmsg.edit(embed=embed)
            return

        data = requests.get("https://nekos.life/api/v2/img/yuri").json()
        yuri = data["url"]

        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=yuri)
        await statusmsg.edit(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["felle"])
    async def trap(self, ctx):
        """Er det en gutt eller en jente?"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        if not ctx.channel.is_nsfw():
            embed = discord.Embed(color=0xFF0000, description=":x: Du må være i en NSFW-kanal")
            await statusmsg.edit(embed=embed)
            return

        data = requests.get("https://nekos.life/api/v2/img/trap").json()
        trap = data["url"]

        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=trap)
        await statusmsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(NSFW(bot))