import discord
import asyncio
from discord.ext import commands

import json
import codecs
import sys
import os
from pathlib import Path
import socket
import requests

class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.is_owner()
    @commands.command()
    async def stopbot(self, ctx):
        embed = discord.Embed(color=0xE67E22, description="Stopper bot...")
        await ctx.send(embed=embed)
        sys.exit("Bot stoppet")


    @commands.is_owner()
    @commands.command()
    async def custommsg(self, ctx, channel: discord.TextChannel=None, *args):
        custommessage = " ".join(args)
        await channel.send(custommessage)

        embed = discord.Embed(color=0xE67E22)
        embed.add_field(name="Sendte", value=custommessage)
        await ctx.send(embed=embed)


    @commands.is_owner()
    @commands.command()
    async def scrapeservers(self, ctx):
        for guild in self.bot.guilds:
            try:
                embed = discord.Embed(color=0xF02B30)
                embed.add_field(name="Name", value=guild.name)
                embed.add_field(name="ID", value=guild.id)
                embed.add_field(name="Owner", value=guild.owner.mention)
                embed.add_field(name="Region", value=guild.region)
                embed.add_field(name="Creation date", value=guild.created_at)
                embed.add_field(name=f"Channels ({len(guild.channels)})", value=[channel.name for channel in guild.channels], inline=False)
                embed.add_field(name="ChannelIDs", value=[channel.id for channel in guild.channels], inline=False)
                embed.add_field(name=f"Roles ({len(guild.roles)})", value=[role.name for role in guild.roles], inline=False)
                embed.add_field(name=f"Members ({len(guild.members)})", value=[member.name for member in guild.members], inline=False)
                embed.add_field(name=f"MemeberIDs", value=[member.id for member in guild.members], inline=False)
                embed.set_thumbnail(url=guild.icon_url)
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(color=0xF02B30, description="ServerScraping feilet. Fortsetter om mulig...")
                await ctx.send(embed=embed)
            

    @commands.is_owner()
    @commands.command(aliases=["listservers"])
    async def listguilds(self, ctx):
        guildlist = []
        for guild in self.bot.guilds:
            guildlist.append(guild.name)
        guilds = "\n".join(guildlist)

        embed = discord.Embed(color=0xE67E22)
        embed.add_field(name="Guilder", value=guilds)
        await ctx.send(embed=embed)


    @commands.is_owner()
    @commands.command()
    async def listusers(self, ctx):
        userlist = []
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.bot:
                    pass
                elif f"{member.name}#{member.discriminator} - {member.id}" in userlist:
                    pass
                else:
                    userlist.append(f"{member.name}#{member.discriminator} - {member.id}")

        while userlist != []:
            users = "\n".join(userlist[:30])
            await ctx.send(f"```{users}```")
            del userlist[:30]


    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, cog):
        try:
            for file in os.listdir("cogs"):
                if file.endswith(".py"):
                    name = file[:-3]
                    if name == cog:
                        try:
                            self.bot.unload_extension(f"cogs.{name}")
                        except:
                            pass
                        embed = discord.Embed(color=0xE67E22, description=f"{cog} har blitt unloadet! :ok_hand:")
                        await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: {cog} er ikke en cog")
            await ctx.send(embed=embed)


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
                        embed = discord.Embed(color=0xE67E22, description=f"{cog} har blitt lastet inn på nytt! :ok_hand:")
                        await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: {cog} er ikke en cog")
            await ctx.send(embed=embed)


    @commands.is_owner()
    @commands.command()
    async def reloadall(self, ctx):
        try:
            for file in os.listdir("cogs"):
                if file.endswith(".py"):
                    name = file[:-3]
                    try:
                        self.bot.unload_extension(f"cogs.{name}")
                    except:
                        pass

                    self.bot.load_extension(f"cogs.{name}")

            embed = discord.Embed(color=0xE67E22, description="Reloadet alle cogs! :ok_hand:")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xFF0000, description=":x: Error!")
            await ctx.send(embed=embed)
    

    @commands.is_owner()
    @commands.command()
    async def localip(self, ctx):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        embed = discord.Embed(color=0xE67E22)
        embed.add_field(name="Lokal ip", value=s.getsockname()[0])
        await ctx.send(embed=embed)
        s.close()


    @commands.is_owner()
    @commands.command()
    async def publicip(self, ctx):
        """inb4 lekker ip-en min"""

        data = requests.get("https://wtfismyip.com/json").json()

        ip = data["YourFuckingIPAddress"]
        location = data["YourFuckingLocation"]
        isp = data["YourFuckingISP"]

        embed = discord.Embed(color=0xE67E22)
        embed.add_field(name="Public ip", value=f"{ip}\n{location}\n{isp}")
        await ctx.send(embed=embed)


    @commands.is_owner()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command()
    async def changepresence(self, ctx, activityType, message, *statusType):

        activities = {
            "playing": 0,
            "listening": 2,
            "watching": 3
        }
        if activityType in activities:
            activityType = activities[activityType]
        else:
            activityType = 0

        statusTypes = {
            "online": discord.Status.online,
            "dnd": discord.Status.dnd,
            "idle": discord.Status.idle,
            "offline": discord.Status.offline
        }
        if statusType in statusTypes:
            statusType = statusTypes[statusType]

        if not statusType:
            statusType = statusTypes["online"]
        try:
            await self.bot.change_presence(status=statusType, activity=discord.Activity(type=activityType, name=message))
            embed = discord.Embed(color=0xE67E22, description="Endret Presence! :ok_hand:")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xFF0000, description=":x: Error!")
            await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def leave(self, ctx, *guildId: int):
        
        if guildId is ():
            guildId = ctx.message.guild.id
        else:
            guildId = guildId[0]

        guild = await self.bot.fetch_guild(guildId)

        comfirmationMsg = await ctx.send(f"Vil du virkelig forlate {guild.name} (`{guild.id}`)?")
        await comfirmationMsg.add_reaction("✅")

        def comfirm(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == "✅"

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=15.0, check=comfirm)
        except asyncio.TimeoutError:
            await ctx.message.delete()
            await comfirmationMsg.delete()
        else:
            await guild.leave()
            try:
                embed = discord.Embed(color=0xE67E22, description="Forlatt guild! :ok_hand:")
                await ctx.send(embed=embed)
            except:
                pass
            
        

def setup(bot):
    bot.add_cog(DevTools(bot))
