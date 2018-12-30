import discord
import asyncio
from discord.ext import commands

import codecs
import json
import requests

class osu:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["osustats", "osuuser", "osuprofile"])
    async def osuprofil(self, ctx, gamemode, bruker):
        """Viser info om en osu! profil\n\nEksmpel: m!osuprofil -GN"""

        user = ctx.message.author

        #   Hent API key
        with codecs.open("config.json", "r", encoding="utf8") as f:
            config = json.load(f)
            osuApiKey = config["osuApiKey"]

        gamemodes = {
            "standard": "0",
            "taiko": "1",
            "ctb": "2",
            "mania": "3"
        }

        gamemode = "0"

        #   Sjekk om gyldig gamemode
        if gamemode in gamemodes:
            gamemode = gamemodes[gamemode]

        #   Velg bruker
        osuUser = bruker

        #   Hent data
        dataurl = f"https://osu.ppy.sh/api/get_user?u={osuUser}&m={gamemode}&k={osuApiKey}"
        data = requests.get(dataurl).json()

        userId = data[0]["user_id"]
        userUrl = f"https://osu.ppy.sh/users/{userId}"
        profilePic = f"http://a.ppy.sh/{userId}"
        username = data[0]["username"]
        level = str(round(float(data[0]["level"]), 2))
        rank = data[0]["pp_rank"]

        #   Sjekk om bruker har spillt nok
        if rank == "#0":
            ctx.send("Brukeren har ikke spillt nok")

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
            embed.set_footer(text=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
            await ctx.send(embed=embed)

            """
            @commands.command(aliases=["osubestplays", "osuplays"])
            async def osubest(self, ctx, gamemode, bruker):
                with codecs.open("config.json", "r", encoding="utf8") as f:
                    config = json.load(f)
                    osuApiKey = config["osuApiKey"]

                #   Select gamemode
                gamemodes = {
                    "standard": "0",
                    "taiko": "1",
                    "ctb": "2",
                    "mania": "3"
                }

                gamemode = "0"
                if gamemode in gamemodes:
                    gamemode = gamemodes[gamemode]

                #   Select user
                osuUser = bruker

                #   Fetch data
                dataurl = f"https://osu.ppy.sh/api/get_user_best?u={osuUser}&m={gamemode}&k={osuApiKey}&limit=5"
                data = requests.get(dataurl).json()
                
                for blablabla in data
                rating = data[number]["rank"]
                pp = str(round(float(data["pp"])))
                maxCombo = data["maxcombo"]
                fc = data["perfect"]
                date = data["date"]
                count50 = data["count50"]
                count100 = data["count100"]
                katu = data["countkatu"]
                count300 = data["count300"]
                geki = data["countgeki"]
                countMiss = data["countmiss"]     
                mods

                #   Embed
                embed = discord.Embed(title=username, color=0xCC5288, url=userUrl)
                embed.set_thumbnail(url=profilePic)
                embed.description = f"<:ScoreSSPlus:476372071014727706>{sshRanks} <:ScoreSS:476372071316848640>{ssRanks} <:ScoreSPlus:476372071342145536>{shRanks} <:ScoreS:476372070989692929>{sRanks} <:ScoreA:476372070976978955>{aRanks}"
                embed.add_field(name="Global Ranking", value=f"#{rank}")
                embed.set_author(name="osu!", icon_url="https://upload.wikimedia.org/wikipedia/commons/d/d3/Osu%21Logo_%282015%29.png")
                embed.set_footer(text=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)

                #   Send Melding
                await ctx.send(embed=embed)
                """

def setup(bot):
    bot.add_cog(osu(bot))