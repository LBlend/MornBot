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
    
        reddit = praw.Reddit(client_id=redditId, client_secret=redditSecret, user_agent="MornBot")

        #   Hent data
        sub = reddit.subreddit("hmmm")
        posts = [post for post in sub.hot(limit=100)]
        random_post_number = random.randint(0, 100)
        submission = posts[random_post_number]

        #   Embed
        embed = discord.Embed(title="Tilfeldig post fra /r/hmmm", url=submission.url, color=0xfaff00)
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def copypasta(self, ctx):
        """Sender en tilfeldig copypasta fra /r/copypasta"""

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
            embed = discord.Embed(title=submission.title, url=submission.url, color=0xfaff00)
            redditor = submission.author
            embed.add_field(name=f"Postet av: {redditor}", value=submission.selftext, inline=False)
            await ctx.send(embed=embed)

        except:
            await ctx.send("**Kunne ikke hente Reddit post**\nPrøv igjen")


def setup(bot):
    bot.add_cog(Reddit(bot))