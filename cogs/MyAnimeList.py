import discord
import asyncio
from discord.ext import commands

import requests

class MyAnimeList:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["myanimelist", "myanimelistprofile", "malprofile"])
    async def mal(self, ctx, medium, bruker):
        """Viser informasjon om en profil på MyAnimeList\n\nEksmpel: m!mal anime Thaun_\nEksempel 2: m!mal manga Thaun_"""

        #   Sjekk for error & Hent data
        try:
            apiUrl = f"https://api.jikan.moe/v3/user/{bruker}"
            data = requests.get(apiUrl).json()

            profilepic = data["image_url"]

        except:
            await ctx.send("Noe gikk galt\nSkriv `m!help mal` for hjelp")
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
       
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MyAnimeList(bot))