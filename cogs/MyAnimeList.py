import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests

with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]

class MyAnimeList:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["myanimelist", "myanimelistprofile", "malprofile"])
    async def mal(self, ctx, medium, bruker):
        """Viser informasjon om en profil på MyAnimeList"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk for error & Hent data
        try:
            data = requests.get(f"https://api.jikan.moe/v3/user/{bruker}").json()

            profilepic = data["image_url"]

        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help mal` for hjelp")
            await statusmsg.edit(embed=embed)
            return

        #   Hent resten av data
        userurl = data["url"]
        brukernavn = data["username"]

        #   Embed
        embed = discord.Embed(title=brukernavn, color=0x2B4FA5, url=userurl)
        embed.set_author(name="MyAnimeList", icon_url="https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png")
        
        #   Sjekk medium
        if medium == "anime":

            #   Hent data
            dagersett = data["anime_stats"]["days_watched"]
            episodersett = data["anime_stats"]["episodes_watched"]
            completed = data["anime_stats"]["completed"]
            watching = data["anime_stats"]["watching"]
            dropped = data["anime_stats"]["dropped"]
            planned = data["anime_stats"]["plan_to_watch"]
            vurdering = data["anime_stats"]["mean_score"]

            #   Embed
            embed.add_field(name="Gjenomsnittlig vurdering", value=str(vurdering))
            embed.add_field(name="Antall dager sett", value=str(dagersett))
            embed.add_field(name="Antall episoder sett", value=str(episodersett))
            embed.add_field(name="Antall animer sett", value=str(completed))
            embed.add_field(name="Ser på nå", value=str(watching), inline=False)
            embed.add_field(name="Planlegger å se", value=str(planned), inline=False)
            embed.add_field(name="Dropped", value=str(dropped), inline=False)
        
        #   Sjekk medium
        elif medium == "manga":
            
            #   Hent data
            dagerlest = data["manga_stats"]["days_read"]
            volumesread = data["manga_stats"]["volumes_read"]
            completed = data["manga_stats"]["completed"]
            reading = data["manga_stats"]["reading"]
            dropped = data["manga_stats"]["dropped"]
            planned = data["manga_stats"]["plan_to_read"]
            vurdering = data["manga_stats"]["mean_score"]

            #   Embed
            embed.add_field(name="Gjenomsnittlig vurdering", value=str(vurdering), inline=True)
            embed.add_field(name="Antall dager lest", value=str(dagerlest), inline=True)
            embed.add_field(name="Antall volumer lest", value=str(volumesread), inline=True)
            embed.add_field(name="Antall mangar lest", value=str(completed), inline=True)
            embed.add_field(name="Leser nå", value=str(reading), inline=False)
            embed.add_field(name="Planlegger å lese", value=str(planned), inline=False)
            embed.add_field(name="Dropped", value=str(dropped), inline=False)
        
        embed.set_thumbnail(url=profilepic)
        embed.set_footer(text=f'{ctx.message.author.name}#{ctx.message.author.discriminator}', icon_url=ctx.message.author.avatar_url)
       
        await statusmsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(MyAnimeList(bot))