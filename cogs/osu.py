import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests
import urllib.parse


with codecs.open("config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    prefix = config["prefix"]
    osuApiKey = config["osuApiKey"]

gamemodes = {
    "standard": "0",
    "taiko": "1",
    "ctb": "2",
    "mania": "3"
}


class osu:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["osustats", "osuuser", "osuprofile"])
    async def osuprofil(self, ctx, bruker, gamemode=None):
        """Viser info om en osu! profil"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        #   Sjekk om gyldig gamemode
        if gamemode in gamemodes:
            gamemode = gamemodes[gamemode]
        else:
            gamemode = "0"

        #   Velg bruker
        osuUser = bruker

        #   Sjekk for error
        try:
            url = "https://osu.ppy.sh/api/get_user?" + urllib.parse.urlencode({"u": osuUser, "m": gamemode, "k": osuApiKey})
            data = requests.get(url).json()

            userId = data[0]["user_id"]

        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: Noe gikk galt\n\nSkriv `{prefix}help osuprofil` for hjelp")
            await statusmsg.edit(embed=embed)
            return

        #   Hent resten av data
        userUrl = f"https://osu.ppy.sh/users/{userId}"
        profilePic = f"http://a.ppy.sh/{userId}"
        username = data[0]["username"]
        level = str(round(float(data[0]["level"]), 2))
        rank = data[0]["pp_rank"]

        #   Sjekk om bruker har spillt nok
        if rank == "#0":
            embed = discord.Embed(color=0xFF0000, description=f":x: Brukeren har ikke spillt nok")
            await statusmsg.edit(embed=embed)

        #   Hent data
        else:
            countryrank = data[0]["pp_country_rank"]
            country = data[0]["country"]
            pp = str(round(float(data[0]["pp_raw"])))
            acc = round(float(data[0]["accuracy"]), 2)
            ssRanks = data[0]["count_rank_ss"]
            sshRanks = data[0]["count_rank_ssh"]
            sRanks = data[0]["count_rank_s"]
            shRanks = data[0]["count_rank_sh"]
            aRanks = data[0]["count_rank_a"]
            playcount = data[0]["playcount"]
            joinDate = data[0]["join_date"]

            #   Embed
            embed = discord.Embed(title=username, color=0xCC5288, url=userUrl)
            embed.set_thumbnail(url=profilePic)
            embed.description = f"<:ScoreSSPlus:476372071014727706>{sshRanks} <:ScoreSS:476372071316848640>{ssRanks} <:ScoreSPlus:476372071342145536>{shRanks} <:ScoreS:476372070989692929>{sRanks} <:ScoreA:476372070976978955>{aRanks}"
            embed.add_field(name="Global Ranking", value=f"#{rank}")
            embed.add_field(name="Country Ranking", value=f":flag_{country.lower()}:#{countryrank}")
            embed.add_field(name="PP", value=pp)
            embed.add_field(name="Accuracy", value=f"{acc}%")
            embed.add_field(name="Level", value=level)
            embed.add_field(name="Play Count", value=playcount)
            embed.set_author(name="osu!", icon_url="https://upload.wikimedia.org/wikipedia/commons/d/d3/Osu%21Logo_%282015%29.png")

            #   Ja, dette er ekte. Ikke klag, det funker 
            embed.set_footer(text=f"Bruker lagd: {joinDate[8:10]}.{joinDate[5:7]}.{joinDate[:4]} {joinDate[11:]}")

            await statusmsg.edit(embed=embed)    


def setup(bot):
    bot.add_cog(osu(bot))