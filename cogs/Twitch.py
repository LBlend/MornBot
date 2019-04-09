import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]

class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["twitchuser", "twitchstream"])
    async def twitch(self, ctx, bruker):
        """Viser informasjon om en Twitch-bruker"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        with codecs.open("config.json", "r", encoding="utf8") as f:
            config = json.load(f)
            twitchApiKey = config["twitchApiKey"]

            try:
                userData = requests.get(f"https://api.twitch.tv/kraken/users/{bruker}?client_id={twitchApiKey}").json()
                followData = requests.get(f"https://api.twitch.tv/kraken/channels/{bruker}/follows?client_id={twitchApiKey}").json()
                streamData = requests.get(f"https://api.twitch.tv/kraken/streams/{bruker}?client_id={twitchApiKey}").json()

                profilePic = userData["logo"]
            except:
                embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help twitch` for hjelp")
                await statusmsg.edit(embed=embed)
                return

            username = userData["display_name"]
            name = userData["name"]
            bio = userData["bio"]
            creationDate = str(userData["created_at"])
            creationDateFormatted = f"{creationDate[8:10]}.{creationDate[5:7]}.{creationDate[:4]}"
            userUrl = f"https://twitch.tv/{name}"
            followers = str(followData["_total"])

            embed = discord.Embed(title=username, color=0x392E5C, url=userUrl)
            embed.set_thumbnail(url=profilePic)
            embed.add_field(name="Bio", value=bio, inline=False)
            embed.add_field(name="Følgere", value=str(followers))
            embed.add_field(name="Bruker lagd", value=creationDateFormatted)
            embed.set_author(name="Twitch", icon_url="http://www.gamergiving.org/wp-content/uploads/2016/03/twitch11.png")
            embed.set_footer(text=f"{ctx.message.author.name}#{ctx.message.author.discriminator}", icon_url=ctx.message.author.avatar_url)

            try:
                streamName = streamData["stream"]["channel"]["status"]
                streamGame = streamData["stream"]["game"]
                streamPhoto = streamData["stream"]["preview"]["large"]
                views = str(streamData["stream"]["viewers"])
                embed.add_field(name=":red_circle: Sender direkte nå", value=f"**Antall som ser på:**\n{views}\n\n**Tittel:**\n{streamName}\n\n**Spill:**\n{streamGame}", inline=False)
                embed.set_image(url=streamPhoto)
            except:
                pass
        
            await statusmsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Twitch(bot))