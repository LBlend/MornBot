import discord
from discord.ext import commands

from requests import get


class Interaksjon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['pat'])
    async def klapp(self, ctx, bruker: discord.Member):
        """Klapp en bruker"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if bruker == ctx.author:
            embed = discord.Embed(
                description='Jeg vet du er ensom, ' +
                            'men du kan ikke klappe deg selv')
            return await status_msg.edit(embed=embed)

        data = get('https://nekos.life/api/v2/img/pat').json()
        returned_data = data['url']

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{ctx.author.mention} klappet {bruker.mention}')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['hug'])
    async def klem(self, ctx, bruker: discord.Member):
        """Gi en bruker en klem"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if bruker == ctx.author:
            embed = discord.Embed(
                description='Jeg vet du er ensom, ' +
                            'men du kan ikke klemme deg selv')
            return await status_msg.edit(embed=embed)

        data = get('https://nekos.life/api/v2/img/hug').json()
        returned_data = data['url']

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{ctx.author.mention} ga {bruker.mention} en klem')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['cuddle'])
    async def kos(self, ctx, bruker: discord.Member):
        """Kos med en bruker"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if bruker == ctx.author:
            embed = discord.Embed(
                description='Jeg vet du er ensom, ' +
                            'men du kan ikke kose med deg selv')
            return await status_msg.edit(embed=embed)

        data = get('https://nekos.life/api/v2/img/cuddle').json()
        returned_data = data['url']

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{ctx.author.mention} ga {bruker.mention} en klem')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def poke(self, ctx, bruker: discord.Member):
        """Poke en bruker"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if bruker == ctx.author:
            embed = discord.Embed(
                description='Jeg vet du er ensom, ' +
                            'men du kan ikke poke deg selv')
            return await status_msg.edit(embed=embed)

        data = get('https://nekos.life/api/v2/img/poke').json()
        returned_data = data['url']

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{ctx.author.mention} poket {bruker.mention}')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['kiss'])
    async def kyss(self, ctx, bruker: discord.Member):
        """Kyss en bruker"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if bruker == ctx.author:
            embed = discord.Embed(
                description='Jeg vet du er ensom, ' +
                            'men du kan ikke kysse deg selv')
            return await status_msg.edit(embed=embed)

        data = get('https://nekos.life/api/v2/img/kiss').json()
        returned_data = data['url']

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{ctx.author.mention} kysset {bruker.mention}')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['tickle'])
    async def kil(self, ctx, bruker: discord.Member):
        """Kil en bruker"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if bruker == ctx.author:
            embed = discord.Embed(
                description='Jeg vet du er ensom, ' +
                            'men du kan ikke kile deg selv')
            return await status_msg.edit(embed=embed)

        data = get('https://nekos.life/api/v2/img/tickle').json()
        returned_data = data['url']

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{ctx.author.mention} kilte {bruker.mention}')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['dum', 'idiot'])
    async def baka(self, ctx, bruker: discord.Member):
        """Bruk når folk er dumme"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if bruker == ctx.author:
            embed = discord.Embed(
                description='Jeg vet du har lav selvtillit, ' +
                            'men du kan ikke kalle deg selv en BAKA')
            return await status_msg.edit(embed=embed)

        data = get('https://nekos.life/api/v2/img/baka').json()
        returned_data = data['url']

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{bruker.mention} er en BAKA')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['spank'])
    async def pisk(self, ctx, *bruker: discord.Member):
        """Pisk en bruker (NSFW)"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        data = get('https://nekos.life/api/v2/img/spank').json()
        returned_data = data['url']

        if not bruker == ctx.author:
            embed = discord.Embed(
                color=0x0085ff,
                description=f'{ctx.author.mention} har en fetisj ' +
                'og pisker seg selv')
            embed.set_image(url=returned_data)
            return await status_msg.edit(embed=embed)

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{ctx.author.mention} pisket {bruker.mention}')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['slå', 'klask'])
    async def slap(self, ctx, bruker: discord.Member):
        """Slå noen"""

        embed = discord.Embed(description='Laster...')
        status_msg = await ctx.send(embed=embed)

        if bruker == ctx.author:
            embed = discord.Embed(
                description='Vi er imot selvskading. Ikke klask deg selv')
            return await status_msg.edit(embed=embed)

        data = get('https://nekos.life/api/v2/img/slap').json()
        returned_data = data['url']

        embed = discord.Embed(
            color=0x0085ff,
            description=f'{ctx.author.mention} klasket {bruker.mention}')
        embed.set_image(url=returned_data)
        await status_msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Interaksjon(bot))
