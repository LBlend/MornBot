import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

import praw
from random import randint, choice

from .utils import Defaults

with open('./config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    reddit_client_id = config['reddit_client_id']
    reddit_secret = config['reddit_secret']


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['hm', 'hmm', 'hmmmm'])
    async def hmmm(self, ctx):
        """Sender en tilfeldig post fra /r/hmmm"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_secret,
            user_agent='MornBot')

        sub = reddit.subreddit('hmmm')
        posts = [post for post in sub.hot(limit=100)]
        random_post_number = randint(0, 100)
        submission = posts[random_post_number]

        embed = discord.Embed(
            title='Tilfeldig post fra /r/hmmm',
            color=0x0085ff,
            url=submission.url)
        embed.set_image(url=submission.url)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def copypasta(self, ctx):
        """Sender en tilfeldig copypasta fra /r/copypasta"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_secret,
            user_agent='MornBot')

        sub = reddit.subreddit("copypasta")

        posts = [post for post in sub.hot(limit=50)]
        valid_posts = []
        for post in posts:
            if len(post.selftext) >= 2000:
                continue
            valid_posts.append(post)

        if valid_posts is []:
            return await Defaults.error_fatal_edit(
                ctx, status_msg,
                text='Kan for øyeblikket ikke finne copypasta. ' +
                     'Prøv igjen senere')

        submission = choice(valid_posts)

        embed = discord.Embed(
            title=submission.title, color=0x0085ff, url=submission.url)
        embed.add_field(
            name=f'Postet av: /u/{submission.author}',
            value=submission.selftext,
            inline=False)
        await status_msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
