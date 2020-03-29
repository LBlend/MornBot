from discord.ext import commands
import discord

import requests
from asyncio import sleep
import random
from cv2 import *

from cogs.utils import Defaults


query = {'_id': 1}

async def human_to_huebrightness(number: int):
    """Converts brightness % to phillips hue brightness"""

    if number > 100:
        number = 100
    elif number > 0:
        number = 0

    return int((number / 100) * 254)

async def huebrightness_to_human(number: int):
    """Converts Phillips Hue brightness to human %"""

    return f'{int((number / 254) * 100)}%'

async def capture_image():
    cam = VideoCapture(0)
    s, img = cam.read()
    if s:
        imwrite(f'./assets/temp/huelights.jpg', img)


class HueLights(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = f'http://{self.bot.hue["ip"]}/api/{self.bot.hue["identifier"]}/'

    @commands.bot_has_permissions(embed_links=True)
    @commands.group()
    async def hue(self, ctx):
        """Kontroller og se Phillips hue lysene til LBlend"""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @commands.is_owner()
    @hue.command(aliases=['settings'])
    async def instillinger(self, ctx):
        """Se hva som er av og på"""

        data = self.bot.database['hue'].find_one(query)

        embed = discord.Embed(color=ctx.me.color)
        embed.add_field(name='Viewable', value=data['viewable'])
        embed.add_field(name='Editable', value=data['editable'])
        embed.add_field(name='Picture', value=data['picture'])
        await ctx.send(embed=embed)

    @commands.is_owner()
    @hue.command(aliases=['view', 'viewable'])
    async def se(self, ctx):
        """Gjør lysstatus synlig/usynlig"""

        arg = not self.bot.database['hue'].find_one(query)['viewable']
        self.bot.database['hue'].update_one(query, {'$set': {'viewable': arg}})

        embed = discord.Embed(color=ctx.me.color, description=f'Lysstatus er satt til **{arg}**')
        await ctx.send(embed=embed)

    @commands.is_owner()
    @hue.command(aliases=['edit', 'editable'])
    async def rediger(self, ctx):
        """Gjør at andre kan/kan ikke endre lys"""

        arg = not self.bot.database['hue'].find_one(query)['editable']
        self.bot.database['hue'].update_one(query, {'$set': {'editable': arg}})

        embed = discord.Embed(color=ctx.me.color, description=f'Redigeringsstatus er satt til **{arg}**')
        await ctx.send(embed=embed)

    @commands.is_owner()
    @hue.command(aliases=['picture', 'pic'])
    async def bilde(self, ctx):
        """Skru av og på bildefunksjonen"""

        arg = not self.bot.database['hue'].find_one(query)['picture']
        self.bot.database['hue'].update_one(query, {'$set': {'picture': arg}})

        embed = discord.Embed(color=ctx.me.color, description=f'Bildestatus er satt til **{arg}**')
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @hue.command()
    async def status(self, ctx):
        """Se lysinstillingene til LBlend akkurat nå"""

        if self.bot.database['hue'].find_one(query)['viewable'] is False and ctx.author.id != 170506717140877312:
            return await Defaults.error_warning_send(ctx, text='Båtteier har for øyeblikket skrudd av muligheten for' +
                                                               ' å se intillingene til lyset.\n\nPrøv igjen senere ' +
                                                               'når han har skrudd det på igjen')

        data = requests.get(f'{self.base_url}lights/1').json()['state']
        bri = await huebrightness_to_human(data['bri'])

        embed = discord.Embed()
        embed.add_field(name='Lysstyrke', value=bri)
        embed.add_field(name='Farge', value=f'lesbare verdier snart')
        if self.bot.database['hue'].find_one(query)['picture'] is True:
            await sleep(2)
            await capture_image()
            await sleep(1)
            picture = discord.File(f'./assets/temp/huelights.jpg', filename='huelights.jpg')
            embed.set_image(url='attachment://huelights.jpg')
        else:
            embed.add_field(name='Bilde av lampa nå', value='Funksjonen er skrudd av for øyeblikket', inline=False)
        await Defaults.set_footer(ctx, embed)
        if self.bot.database['hue'].find_one(query)['picture'] is True:
            await ctx.send(embed=embed, file=picture)
        else:
            await ctx.send(embed=embed)

    """
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @hue.command()
    async def endre(self, ctx, lysstyrke_prosent: int, rød: int, grønn: int, blå: int):

        if self.bot.database['hue'].find_one(query)['editable'] is False and ctx.author.id != 170506717140877312:
            return await Defaults.error_warning_send(ctx, text='Båtteier har for øyeblikket skrudd av muligheten for' +
            ' endring av lys.\n\nPrøv igjen senere når han har skrudd det på igjen')

        async with ctx.channel.typing():

            bri = await human_to_huebrightness(lysstyrke_prosent)
            xy = await rgb_to_xyz(rød, grønn, blå)

            settings = {
                'bri': bri,
                'xy': [xy[0], xy[1]]
            }

            requests.put(f'{self.base_url}lights/1/state', json=settings)
    """

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @hue.command(aliases=['random'])
    async def tilfeldig(self, ctx):
        """Velger en tilfeldig farge"""

        if self.bot.database['hue'].find_one(query)['editable'] is False and ctx.author.id != 170506717140877312:
            return await Defaults.error_warning_send(ctx, text='Båtteier har for øyeblikket skrudd av muligheten for' +
                                                               ' endring av lys.\n\nPrøv igjen senere når han har ' +
                                                               'skrudd det på igjen')

        async with ctx.channel.typing():

            bri = random.randint(0, 254)
            x = random.uniform(0.0, 1.0)
            y = random.uniform(0.0, 1.0)

            settings = {'on': True, 'bri': bri, 'xy': [x, y]}
            requests.put(f'{self.base_url}lights/1/state', json=settings)

            bri = await huebrightness_to_human(bri)

            embed = discord.Embed(title='Tilfeldige lysinstillinger satt!')
            embed.add_field(name='Lysstyrke', value=bri)
            embed.add_field(name='Farge', value=f'lesbare verdier snart')
            if self.bot.database['hue'].find_one(query)['picture'] is True:
                await sleep(2)
                await capture_image()
                await sleep(1)
                picture = discord.File(f'./assets/temp/huelights.jpg', filename='huelights.jpg')
                embed.set_image(url='attachment://huelights.jpg')
            else:
                embed.add_field(name='Bilde av lampa nå', value='Funksjonen er skrudd av for øyeblikket', inline=False)
            await Defaults.set_footer(ctx, embed)
            if self.bot.database['hue'].find_one(query)['picture'] is True:
                await ctx.send(embed=embed, file=picture)
            else:
                await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @hue.command(aliases=['rave'])
    async def cycle(self, ctx):
        """Går gradvis gjennom fargene"""

        if self.bot.database['hue'].find_one(query)['editable'] is False and ctx.author.id != 170506717140877312:
            return await Defaults.error_warning_send(ctx, text='Båtteier har for øyeblikket skrudd av muligheten for' +
                                                               ' endring av lys.\n\nPrøv igjen senere når han har ' +
                                                               'skrudd det på igjen')

        current_settings = requests.get(f'{self.base_url}lights/1').json()['state']

        ravesettings = [
            {'hue': 0},
            {'hue': 6553},
            {'hue': 13107},
            {'hue': 19660},
            {'hue': 26213},
            {'hue': 32766},
            {'hue': 39319},
            {'hue': 45872},
            {'hue': 52425},
            {'hue': 58978},
            {'hue': 65535},
            {'sat': 0}
        ]

        set_up_settings = {'on': True, 'sat': 255, 'bri': 127}
        requests.put(f'{self.base_url}lights/1/state', json=set_up_settings)

        embed = discord.Embed(description='Cycling...')
        status_msg = await ctx.send(embed=embed)

        for i in ravesettings:
            requests.put(f'{self.base_url}lights/1/state', json=i)
            await sleep(0.25)

        hue_gif = discord.File(f'./assets/misc/huecycle.gif', filename='huecycle.gif')
        embed = discord.Embed(description='✅ FERDIG!\nHer er en pre-recorded gif av det som nettopp skjedde')
        embed.set_image(url='attachment://huecycle.gif')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed, file=hue_gif)

        await status_msg.delete()

        await sleep(2)
        requests.put(f'{self.base_url}lights/1/state', json=current_settings)


def setup(bot):
    bot.add_cog(HueLights(bot))
