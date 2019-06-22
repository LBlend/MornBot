from discord.ext import commands
import discord

from codecs import open
from json import load as json_load
import locale

import praw
from random import randint, choice
from datetime import datetime

from cogs.utils import Defaults

with open('./config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    reddit_client_id = config['reddit_client_id']
    reddit_secret = config['reddit_secret']

locale.setlocale(locale.LC_ALL, '')


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def subreddit(self, ctx, subreddit: str):
        """Få info om en subreddit"""

        async with ctx.channel.typing():

            reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_secret, user_agent='MornBot')

            sub = reddit.subreddit(subreddit)

            try:
                created_at = datetime.fromtimestamp(
                    sub.created_utc).strftime('%d.%m.%Y')
            except:
                return await Defaults.error_fatal_send(ctx, text='Subredditen finnes ikke eller så ' +
                                                                 'har jeg ikke tilgang på den')

            nsfw = 'Nei'
            if sub.over18:
                nsfw = 'Ja'

            subscribers = locale.format_string('%d', sub.subscribers, grouping=True)

            embed = discord.Embed(title=f'/r/{sub.display_name}', color=ctx.me.color,
                                  url=f'https://www.reddit.com/r/{sub.display_name}')
            embed.add_field(name='Abonnenter', value=subscribers)
            embed.add_field(name='Opprettet', value=created_at)
            embed.add_field(name='NSFW', value=nsfw)
            embed.add_field(name='Beskrivelse', value=sub.public_description, inline=False)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['reddituser', 'redditbruker'])
    async def redditor(self, ctx, bruker: str):
        """Få info om en redditor"""

        async with ctx.channel.typing():

            reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_secret, user_agent='MornBot')

            bruker = reddit.redditor(bruker)

            try:
                created_at = datetime.fromtimestamp(
                    bruker.created_utc).strftime('%d.%m.%Y')
            except:
                return await Defaults.error_fatal_send(ctx, text='Brukeren finnes ikke eller så ' +
                                                                 'har jeg ikke tilgang på den')

            notable_mentions = ''
            if bruker.is_employee:
                notable_mentions += 'Reddit Staff\n'
            if bruker.is_gold:
                notable_mentions += 'Reddit Gold'

            link_karma = locale.format_string('%d', bruker.link_karma, grouping=True)
            comment_karma = locale.format_string('%d', bruker.comment_karma, grouping=True)

            embed = discord.Embed(title=f'/u/{bruker.name}', color=ctx.me.color,
                                  url=f'https://www.reddit.com/u/{bruker.name}')
            if notable_mentions is not '':
                embed.description = notable_mentions
            embed.set_thumbnail(url=bruker.icon_img)
            embed.add_field(name='Post Karma', value=link_karma, inline=False)
            embed.add_field(name='Comment Karma', value=comment_karma, inline=False)
            embed.add_field(name='Opprettet', value=created_at)
            if bruker.trophies() != []:
                trophies = []
                for trophy in bruker.trophies():
                    trophies.append(trophy.name)
                trophies = ', '.join(trophies)
                if len(trophies) < 1000:
                    embed.add_field(name='Trofeer', value=trophies, inline=False)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def redditimg(self, ctx, subreddit: str):
        """Sender et bilde fra en tilfeldig post fra subreddit"""

        async with ctx.channel.typing():

            reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_secret, user_agent='MornBot')

            sub = reddit.subreddit(subreddit)
            try:
                if sub.over18:
                    if not ctx.channel.is_nsfw():
                        return await Defaults.error_fatal_send(ctx, text='Du må være i en NSFW-Kanal')
            except:
                return await Defaults.error_fatal_send(ctx, text='Subredditen finnes ikke eller ' +
                                                                 'så har jeg ikke tilgang på den')

            posts = []
            for post in sub.hot(limit=100):
                if not ctx.channel.is_nsfw() and post.over_18:
                    continue
                if 'i.redd.it' in post.url or 'i.imgur.com' in post.url:
                    if post.url.endswith('v'):
                        post.url = post.url[:-1]
                    posts.append(post)
            random_post_number = randint(0, len(posts))
            try:
                submission = posts[random_post_number]
            except IndexError:
                return await Defaults.error_fatal_send(ctx, text='Fant ingen posts')

            embed = discord.Embed(title=f'Tilfeldig bildepost fra /r/{sub.display_name}',
                                  color=ctx.me.color, url=submission.url)
            embed.set_image(url=submission.url)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def copypasta(self, ctx):
        """Sender en tilfeldig copypasta fra /r/copypasta"""

        async with ctx.channel.typing():

            reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_secret, user_agent='MornBot')

            sub = reddit.subreddit('copypasta')

            posts = [post for post in sub.hot(limit=50)]
            valid_posts = []
            for post in posts:
                if len(post.selftext) >= 2000:
                    continue
                if post.spoiler:
                    continue
                if not ctx.channel.is_nsfw() and post.over_18:
                    continue
                valid_posts.append(post)

            if valid_posts is []:
                return await Defaults.error_fatal_send(ctx, text='Kan for øyeblikket ikke finne copypasta. ' +
                                                                 'Prøv igjen senere')

            submission = choice(valid_posts)

            if not ctx.channel.is_nsfw() and submission.over_18:
                return await Defaults.error_fatal_send(ctx, text='Du må være i en NSFW-Kanal')

            embed = discord.Embed(title=f'{submission.title}', color=ctx.me.color, url=submission.url,
                                  description=f'*/u/{submission.author}*\n\n{submission.selftext}')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reddit(bot))
