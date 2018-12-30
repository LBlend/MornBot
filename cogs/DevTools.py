import discord
import asyncio
from discord.ext import commands

import json
import codecs
import sys
import os
from pathlib import Path

class DevTools:
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def stopbot(self, ctx):
        await ctx.send("Stopper bot")
        sys.exit("Bot stoppet")

    @commands.is_owner()
    @commands.command()
    async def custommsg(self, ctx, channel: discord.TextChannel=None, *args):
        custommessage = " ".join(args)
        await channel.send(custommessage)
        await ctx.send(f"Sendte:\n{custommessage}")

    @commands.is_owner()
    @commands.command()
    async def scrapeservers(self, ctx):
        for guild in self.bot.guilds:
            embed = discord.Embed(color=0xF02B30)
            embed.add_field(name="Name", value=guild.name)
            embed.add_field(name="ID", value=guild.id)
            embed.add_field(name="Owner", value=f"<@{guild.owner.id}>")
            embed.add_field(name="Region", value=guild.region)
            embed.add_field(name="Creation date", value=guild.created_at)
            embed.add_field(name=f"Channels ({len(guild.channels)})", value=[channel.name for channel in guild.channels], inline=False)
            embed.add_field(name="ChannelIDs", value=[channel.id for channel in guild.channels], inline=False)
            embed.add_field(name=f"Roles ({len(guild.roles)})", value=[role.name for role in guild.roles], inline=False)
            embed.add_field(name=f"Members ({len(guild.members)})", value=[member.name for member in guild.members], inline=False)
            embed.add_field(name=f"MemeberIDs", value=[member.id for member in guild.members], inline=False)
            embed.set_thumbnail(url=guild.icon_url)
            await ctx.send(embed=embed)
            #await ctx.send("Sorry mac! Æ hør bare på homseungen sin kommando <3")

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, cog):

        try:
            for file in os.listdir("cogs"):
                if file.endswith(".py"):
                    name = file[:-3]
                    if name == cog:
                        try:
                            self.bot.unload_extension(f"cogs.{name}")
                        except:
                            pass
                        self.bot.load_extension(f"cogs.{name}")
                        await ctx.send(f"{cog} har blitt lastet inn på nytt")
        except:
            await ctx.send(f"{cog} er ikke en cog")

def setup(bot):
    bot.add_cog(DevTools(bot))
