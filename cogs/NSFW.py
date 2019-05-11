import discord
from discord.ext import commands

from requests import get


class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['bj'])
    async def blowjob(self, ctx):
        """Blowjob GIF"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        data = get('https://nekos.life/api/v2/img/bj').json()
        returned_data = data['url']

        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def yuri(self, ctx):
        """Yuri"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        data = get('https://nekos.life/api/v2/img/yuri').json()
        returned_data = data['url']

        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['felle'])
    async def trap(self, ctx):
        """Er det en gutt eller en jente?"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        data = get('https://nekos.life/api/v2/img/trap').json()
        returned_data = data['url']

        embed = discord.Embed(color=0x0085ff)
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(NSFW(bot))
