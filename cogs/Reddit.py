import discord
import asyncio
from discord.ext import commands

import codecs
import json
import random
import praw

with codecs.open("./config.json", "r", encoding="utf8") as f:
    config = json.load(f)
    redditId = config["redditId"]
    redditSecret = config["redditSecret"]

class Reddit:
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["hm", "hmm", "hmmmm"])
    async def hmmm(self, ctx):
        """Sender en tilfeldig post fra /r/hmmm"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)
    
        reddit = praw.Reddit(client_id=redditId, client_secret=redditSecret, user_agent="MornBot")

        #   Hent data
        sub = reddit.subreddit("hmmm")
        posts = [post for post in sub.hot(limit=100)]
        random_post_number = random.randint(0, 100)
        submission = posts[random_post_number]

        #   Embed
        embed = discord.Embed(title="Tilfeldig post fra /r/hmmm", url=submission.url, color=0x0085ff)
        embed.set_image(url=submission.url)
        await statusmsg.edit(embed=embed)

    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def copypasta(self, ctx):
        """Sender en tilfeldig copypasta fra /r/copypasta"""

        embed = discord.Embed(description="Laster...")
        statusmsg = await ctx.send(embed=embed)

        reddit = praw.Reddit(client_id=redditId, client_secret=redditSecret, user_agent="MornBot")
        
        #   Hent data
        try:
            sub = reddit.subreddit("copypasta")
            posts = [post for post in sub.hot(limit=50)]
            random_post_number = random.randint(0, 50)
            submission = posts[random_post_number]
            while len(submission.selftext) >= 1024:
                random_post_number = random.randint(0, 50)
                submission = posts[random_post_number]
                if len(submission.selftext) < 1024:
                    submission = posts[random_post_number]
                    break

            #   Embed
            embed = discord.Embed(title=submission.title, url=submission.url, color=0x0085ff)
            redditor = submission.author
            embed.add_field(name=f"Postet av: {redditor}", value=submission.selftext, inline=False)
            await statusmsg.edit(embed=embed)

        except:
            embed = discord.Embed(color=0xFF0000, description=f":x: **Kunne ikke hente Reddit post**\n\nPrøv igjen")
            await statusmsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))