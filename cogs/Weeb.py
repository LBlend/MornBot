from discord.ext import commands
import discord

from requests import get

from cogs.utils import Defaults


class Weeb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def raphtalia(self, ctx):
        """Tilfeldig bilde av Raphtalia"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/raphtalia').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def megumin(self, ctx):
        """Tilfeldig bilde av Megumin"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/megumin').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def rem(self, ctx):
        """Tilfeldig bilde av Rem"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/rem').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def emilia(self, ctx):
        """Tilfeldig bilde av Emilia"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/emilia').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def kaguya(self, ctx):
        """Tilfeldig bilde av Kaguya"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/kaguya').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def chika(self, ctx):
        """Tilfeldig bilde av Chika"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/chika').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def kumiko(self, ctx):
        """Tilfeldig bilde av Kumiko"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/kumiko').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def vignette(self, ctx):
        """Tilfeldig bilde av Vignette"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/vignette').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)
    
    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(name='k-on')
    async def k_on(self, ctx):
        """Tilfeldig bilde av noe K-ON-relatert"""

        async with ctx.channel.typing():
            
            try:
                data = get('https://api.lblend.moe/k-on').json()
                returned_data = data['data']['image_url']
            except:
                return Defaults.error_fatal_send(ctx, text='API-forespørsel feilet!')

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['pat'])
    async def klapp(self, ctx, bruker: discord.Member):
        """Klapp en bruker"""

        async with ctx.channel.typing():

            if bruker == ctx.author:
                embed = discord.Embed(description='Jeg vet du er ensom, men du kan ikke klappe deg selv')
                return await ctx.send(embed=embed)

            data = get('https://nekos.life/api/v2/img/pat').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color, description=f'{ctx.author.mention} klappet {bruker.mention}')
            embed.set_image(url=returned_data)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['hug'])
    async def klem(self, ctx, bruker: discord.Member):
        """Gi en bruker en klem"""

        async with ctx.channel.typing():

            if bruker == ctx.author:
                embed = discord.Embed(description='Jeg vet du er ensom, men du kan ikke klemme deg selv')
                return await ctx.send(embed=embed)

            data = get('https://nekos.life/api/v2/img/hug').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color, description=f'{ctx.author.mention} ga {bruker.mention} en klem')
            embed.set_image(url=returned_data)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['cuddle'])
    async def kos(self, ctx, bruker: discord.Member):
        """Kos med en bruker"""

        async with ctx.channel.typing():

            if bruker == ctx.author:
                embed = discord.Embed(description='Jeg vet du er ensom, men du kan ikke kose med deg selv')
                return await ctx.send(embed=embed)

            data = get('https://nekos.life/api/v2/img/cuddle').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color, description=f'{ctx.author.mention} ga {bruker.mention} en klem')
            embed.set_image(url=returned_data)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def poke(self, ctx, bruker: discord.Member):
        """Poke en bruker"""

        async with ctx.channel.typing():

            if bruker == ctx.author:
                embed = discord.Embed(description='Jeg vet du er ensom, men du kan ikke poke deg selv')
                return await ctx.send(embed=embed)

            data = get('https://nekos.life/api/v2/img/poke').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color, description=f'{ctx.author.mention} poket {bruker.mention}')
            embed.set_image(url=returned_data)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['kiss'])
    async def kyss(self, ctx, bruker: discord.Member):
        """Kyss en bruker"""

        async with ctx.channel.typing():

            if bruker == ctx.author:
                embed = discord.Embed(description='Jeg vet du er ensom, men du kan ikke kysse deg selv')
                return await ctx.send(embed=embed)

            data = get('https://nekos.life/api/v2/img/kiss').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color, description=f'{ctx.author.mention} kysset {bruker.mention}')
            embed.set_image(url=returned_data)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['tickle'])
    async def kil(self, ctx, bruker: discord.Member):
        """Kil en bruker"""

        async with ctx.channel.typing():

            if bruker == ctx.author:
                embed = discord.Embed(description='Jeg vet du er ensom, men du kan ikke kile deg selv')
                return await ctx.send(embed=embed)

            data = get('https://nekos.life/api/v2/img/tickle').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color, description=f'{ctx.author.mention} kilte {bruker.mention}')
            embed.set_image(url=returned_data)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['dum', 'idiot'])
    async def baka(self, ctx, bruker: discord.Member):
        """Bruk når folk er dumme"""

        async with ctx.channel.typing():

            if bruker == ctx.author:
                embed = discord.Embed(
                    description='Jeg vet du har lav selvtillit, men du kan ikke kalle deg selv en BAKA')
                return await ctx.send(embed=embed)

            data = get('https://nekos.life/api/v2/img/baka').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color, description=f'{bruker.mention} er en BAKA')
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['slå', 'klask'])
    async def slap(self, ctx, bruker: discord.Member):
        """Slå noen"""

        async with ctx.channel.typing():

            if bruker == ctx.author:
                embed = discord.Embed(description='Vi er imot selvskading. Ikke klask deg selv')
                return await ctx.send(embed=embed)

            data = get('https://nekos.life/api/v2/img/slap').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color, description=f'{ctx.author.mention} klasket {bruker.mention}')
            embed.set_image(url=returned_data)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def smug(self, ctx):
        """Sender et smug bilde"""

        async with ctx.channel.typing():

            data = get('https://nekos.life/api/v2/img/smug').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['bakgrunn'])
    async def wallpaper(self, ctx):
        """Sender et tilfeldig bakgrunnsbilde (NSFW)"""

        async with ctx.channel.typing():

            data = get('https://nekos.life/api/v2/img/wallpaper').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['bj'])
    async def blowjob(self, ctx):
        """Blowjob GIF"""

        async with ctx.channel.typing():

            data = get('https://nekos.life/api/v2/img/bj').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def yuri(self, ctx):
        """Yuri"""

        async with ctx.channel.typing():

            data = get('https://nekos.life/api/v2/img/yuri').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['felle'])
    async def trap(self, ctx):
        """Er det en gutt eller en jente?"""

        async with ctx.channel.typing():

            data = get('https://nekos.life/api/v2/img/trap').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.is_nsfw()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['spank'])
    async def pisk(self, ctx, *bruker: discord.Member):
        """Pisk en bruker (NSFW)"""

        async with ctx.channel.typing():

            data = get('https://nekos.life/api/v2/img/spank').json()
            returned_data = data['url']

            if not bruker == ctx.author:
                embed = discord.Embed(color=ctx.me.color,
                                      description=f'{ctx.author.mention} har en fetisj og pisker seg selv')
                embed.set_image(url=returned_data)
                await ctx.send(embed=embed)

            embed = discord.Embed(color=ctx.me.color, description=f'{ctx.author.mention} pisket {bruker.mention}')
            embed.set_image(url=returned_data)
            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Weeb(bot))
