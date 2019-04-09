import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests
from datetime import datetime

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]

class Anilist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["anilistprofile", "anilistprofil",])
    async def anilist(self, ctx, bruker: str):
        """Viser informasjon om en profil på Anilist"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        query = '''
        query ($name: String) {
        User (name: $name) {
            name
            siteUrl
            updatedAt
            avatar {
                medium
            }
            options {
                profileColor
            }
            stats {
                watchedTime
                animeStatusDistribution {
                    amount
                }
                animeListScores {
                    meanScore
                }
            }
        }
        }
        '''
        variables = {
            "name": bruker
        }

        try:
            data = requests.post("https://graphql.anilist.co", json={"query": query, "variables": variables}).json()
            userUrl = data["data"]["User"]["siteUrl"]
        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Fant ikke bruker\n\nSkriv `{prefix}help anilist` for hjelp")
            await statusmsg.edit(embed=embed)
            return

        userName = data["data"]["User"]["name"]
        profilePic = data["data"]["User"]["avatar"]["medium"]
        rating = data["data"]["User"]["stats"]["animeListScores"]["meanScore"]
        lastUpdated = data["data"]["User"]["updatedAt"]
        lastUpdated = datetime.fromtimestamp(lastUpdated).strftime("%d.%m.%Y %H:%M")
        nowTime = datetime.now().strftime("%d.%m.%Y %H:%M")
        daysWatched = round(data["data"]["User"]["stats"]["watchedTime"] / 1440, 1)
        watching = data["data"]["User"]["stats"]["animeStatusDistribution"][0]["amount"]
        planning = data["data"]["User"]["stats"]["animeStatusDistribution"][1]["amount"]
        completed = data["data"]["User"]["stats"]["animeStatusDistribution"][2]["amount"]
        dropped = data["data"]["User"]["stats"]["animeStatusDistribution"][3]["amount"]

        color = data["data"]["User"]["options"]["profileColor"]
        colors = {
            "blue": 0x3db4f2,
            "purple": 0xc063ff,
            "pink": 0xFC9DD6,
            "orange": 0xEF881A,
            "red": 0xE13333,
            "green": 0x4CCA51,
            "gray": 0x677B94
        }
        if color in colors:
            color = colors[color]
        else:
            color = 0x3db4f2
        
        embed = discord.Embed(title=userName, color=color, url=userUrl)
        embed.set_author(name="Anilist", icon_url="https://avatars3.githubusercontent.com/u/18018524?s=200&v=4")
        embed.set_thumbnail(url=profilePic)
        if rating != None:
            embed.add_field(name="Gjennomsnittlig vurdering", value=rating)
        embed.add_field(name="Antall dager sett", value=daysWatched)
        embed.add_field(name="Antall animer sett", value=completed)
        embed.add_field(name="Ser på nå", value=watching, inline=False)
        embed.add_field(name="Planlegger å se", value=planning, inline=False)
        embed.add_field(name="Droppet", value=dropped, inline=False)
        embed.set_footer(text=f"(Norske tider) Oppdatert: {lastUpdated} | Tid nå: {nowTime}")
        
        await statusmsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Anilist(bot))