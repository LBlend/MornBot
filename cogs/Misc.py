from discord.ext import commands
import discord

from codecs import open
from json import load as json_load
import locale

from requests import get
from urllib import parse
from random import randint, choice
from hashlib import md5
from bs4 import BeautifulSoup
from datetime import datetime
from re import sub, split
from PIL import Image, ImageDraw, ImageFont
from os import remove

from cogs.utils import Defaults, LBlend_utils

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']

locale.setlocale(locale.LC_ALL, '')


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['woof', 'doggo', 'dog', 'hund', 'bikkje'])
    async def voff(self, ctx):
        """Sender bilde av en tilfeldig bissevoff"""

        async with ctx.channel.typing():

            data = get('https://nekos.life/api/v2/img/woof').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['meow', 'nya'])
    async def mjau(self, ctx):
        """Sender bilde av en tilfeldig katt"""

        async with ctx.channel.typing():

            data = get('https://nekos.life/api/v2/img/meow').json()
            returned_data = data['url']

            embed = discord.Embed(color=ctx.me.color)
            embed.set_image(url=returned_data)
            await Defaults.set_footer(ctx, embed)
            if ctx.guild.id == 297798952538079233:
                return await ctx.send(
                    content='<@516234701221134346> er glad i katter',
                    embed=embed)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def drepmeg(self, ctx):
        """Dreper deg"""

        await ctx.send("Du er død nå")

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def sql(self, ctx):
        """Ber LBLend om å lære seg SQL"""

        lblend = await self.bot.fetch_user(170506717140877312)
        await ctx.send(f'{lblend.mention} LÆR DEG SQL NÅÅÅÅ!')

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['kukstørrelse', 'pikkstørrelse'])
    async def dicksize(self, ctx, bruker: discord.Member=None):
        """Se hvor liten pikk du har"""

        if not bruker:
            bruker = ctx.author

        user_id = bruker.id

        def hash_dicksize(user_id, upper, lower):
            dickhash = md5(str(user_id).encode('utf-8')).hexdigest()
            return int(int(dickhash[11:13], 16)*(upper-lower)/255 + lower)

        # Må jo gi meg selv en stor kuk
        if bruker.id == 170506717140877312:
            dick_size = 69
        elif bruker.id == 202745416062599168:
            dick_size = 0
        elif bruker.id == 142580278940925953:
            dick_size = 14
        else:
            dick_size = hash_dicksize(user_id, 25, 2)

        dick_drawing = '=' * dick_size

        embed = discord.Embed(color=bruker.color)
        embed.set_author(
            name=f'{bruker.name}#{bruker.discriminator}',
            icon_url=bruker.avatar_url)
        if bruker.id == 209305971066011648:
            embed.add_field(name='Kukstørrelse', value=f'18.1 cm lang\n16.5 cm girth')
        else:
            embed.add_field(name='Kukstørrelse', value=f'{dick_size} cm\n8{dick_drawing}D')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def roll(self, ctx):
        """Gir deg et tilfeldig tall"""

        embed = discord.Embed(color=ctx.me.color, description=randint(0, 100))
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(name='8ball')
    async def ball8(self, ctx, *, spørsmål: str):
        """Svarer på dine dypeste spørsmål"""

        if spørsmål[-1:] != '?':
            return await Defaults.error_warning_send(ctx, text='Du må stille meg et spørsmål da dømdøm!')

        answers = [
            'Det er sannsynlig',
            'Uten tvil',
            'Ja',
            'Man kan vel si det ja',
            'Ehm, tror det er best vi ikke snakker om det jeg :sweat_smile:',
            'нет',
            'Nei ass',
            'Er ikke så sannsynlig',
            'I følge mine beregninger... nei'
        ]

        embed = discord.Embed(color=ctx.me.color, description=choice(answers))
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['reverse'])
    async def reverser(self, ctx, *, tekst):
        """Reverserer tekst"""

        embed = discord.Embed(color=ctx.me.color, description=tekst[::-1])
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['owoify', 'uwu'])
    async def owo(self, ctx, *, tekst: str):
        """Oversetter teksten din til owo"""

        owo_rules = {
            'r': 'w',
            'l': 'w',
            'R': 'W',
            'L': 'W',
            'n': 'ny',
            'N': 'Ny',
            'ove': 'uv'
        }
        for key, value in owo_rules.items():
            tekst = sub(key, value, tekst)
        # https://kaomoji.moe/

        if not tekst or len(tekst) >= 1000:
            return await Defaults.error_warning_send(ctx, text='Teksten er for lang')

        embed = discord.Embed(color=ctx.me.color, description=tekst)
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['urbandictionary', 'dictionary', 'ordbok'])
    async def urban(self, ctx, *, ord: str):
        """Sjekk definisjonen av et ord"""

        async with ctx.channel.typing():

            try:
                url = 'https://api.urbandictionary.com/v0/define?' + parse.urlencode({'term': ord})
                data = get(url).json()
                urban_url = data['list'][0]['permalink']
            except IndexError:
                return await Defaults.error_fatal_send(ctx, text='Fant ingen definisjon for dette ordet!')

            index = 0
            for definition in data['list'][index]:
                definition = sub(r';|\[|\]', '', data['list'][index]['definition'])
                example = sub(r';|\[|\]', '', data['list'][index]['example'])
                if len(definition) < 1024 and len(example) < 1024:
                    break
                index += 1
            word = data['list'][index]['word']
            urban_url = data['list'][index]['permalink']
            submitter = data['list'][index]['author']
            upvotes = data['list'][index]['thumbs_up']
            upvotes = locale.format_string('%d', upvotes, grouping=True)
            downvotes = data['list'][index]['thumbs_down']
            downvotes = locale.format_string('%d', downvotes, grouping=True)

            embed = discord.Embed(title=word, color=ctx.me.color, url=urban_url,
                                  description=f'**Definert av:** {submitter}')
            embed.set_author(name='Urban Dictionary', icon_url='https://a2.mzstatic.com/us/r30/Purple/v4/dd/ef/75/' +
                                                               'ddef75c7-d26c-ce82-4e3c-9b07ff0871a5/mzl.yvlduoxl.png')
            embed.add_field(name='Definisjon', value=definition)
            embed.add_field(name='Eksempel', value=example, inline=False)
            embed.add_field(name='Vurdering', value=f':thumbsup: {upvotes} / :thumbsdown: {downvotes}', inline=False)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=['isitdown', 'checksite'])
    async def isitup(self, ctx, nettside: str):
        """Sjekk om en nettside er oppe"""

        async with ctx.channel.typing():

            nettside = await LBlend_utils.input_sanitizer(nettside.lower())

            data = get(f'https://isitup.org/{nettside}')
            scraped = BeautifulSoup(data.text, 'html.parser')
            status = scraped.find('p').get_text()
            try:
                nettside = scraped.find(class_='domain').get_text()
            except AttributeError:
                return await Defaults.error_warning_send(ctx, text='Du må skrive URLen i dette formatet:\n`google.com`')
            website_url = scraped.find(class_='domain')['href']

            embed = discord.Embed(title=nettside.lower(), url=website_url, timestamp=datetime.utcnow())

            if status[-6:] == 'is up.':
                status = 'Oppe!'
                ping = scraped.find(class_='smaller').get_text()
                pinglist = []
                for i in ping.split():
                    if i.isdigit():
                        pinglist.append(i)
                embed.add_field(name='📶 Ping', value=f'{pinglist[0]} ms')
                embed.color = 0x2ECC71
            else:
                status = 'Nede!'
                embed.color = 0xff0000

            embed.add_field(name='🔌 Status', value=status)
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['clapify'])
    async def klappifiser(self, ctx, *, tekst):
        """Klapppifiserer teksten din"""

        if not tekst or len(tekst) >= 1000:
            return await Defaults.error_warning_send(ctx, text='Teksten er for lang')

        tekst = sub(' ', '👏', tekst)

        embed = discord.Embed(color=ctx.me.color, description=f'**{tekst.upper()}**')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['video'])
    async def videochat(self, ctx):
        """Få link til videochat"""

        async with ctx.channel.typing():

            try:
                voice_channel_id = ctx.author.voice.channel.id
            except AttributeError:
                return await Defaults.error_warning_send(ctx, text='Du er ikke koblet til en talekanal')

            link = f'https://canary.discordapp.com/channels/{ctx.guild.id}/{voice_channel_id}'
            embed = discord.Embed(title=f'📷 Videochat: {ctx.author.voice.channel.name}', color=ctx.me.color,
                                  description=f'[Trykk her for å bli med i videochat]({link})')
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['timezone', 'tid', 'tidssone', 'klokken'])
    async def klokka(self, ctx, kontinent, by):
        """Se hvor mye klokka er i et bestemt område"""

        async with ctx.channel.typing():

            kontinent = await LBlend_utils.input_sanitizer(kontinent)
            by = await LBlend_utils.input_sanitizer(by)

            try:
                data = get(f'http://worldtimeapi.org/api/timezone/{kontinent.capitalize()}/{by.capitalize()}').json()
                timezone = data['timezone']
            except KeyError:
                return await Defaults.error_warning_send(ctx, text='Kunne ikke finne sted/tidssone')

            timezone = split('/', timezone)
            timezone_local = data['abbreviation']
            timezone_utc = data['utc_offset']
            time_norway = datetime.now().strftime('%H:%M\n%d.%m.%Y')

            time = data['datetime']
            time_formatted = f'{time[11:16]}\n{time[8:10]}.{time[5:7]}.{time[:4]}'

            daylight_savings = data['dst']
            if daylight_savings is False:
                daylight_savings = 'Nei'
            else:
                daylight_savings = 'Ja'

            embed = discord.Embed(title=f'Klokka i {timezone[1]}', color=0x0085ff, timestamp=datetime.utcnow())
            embed.add_field(name='Klokka', value=time_formatted)
            embed.add_field(name='Klokka i Norge', value=time_norway)
            embed.add_field(name='Sommertid', value=daylight_savings)
            embed.add_field(name='UTC tidssone', value=timezone_utc)
            embed.add_field(name='Standard tidssone for sted', value=timezone_local)
            embed.set_footer(text='🕓 Klokka i din tidssone ->')
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['country'])
    async def land(self, ctx, *, land: str):
        """Se info om et land"""

        async with ctx.channel.typing():
            
            land = await LBlend_utils.input_sanitizer(land)

            try:
                data = get(f'https://restcountries.eu/rest/v2/name/{land}').json()
                name = data[0]['name']
            except KeyError:
                return await Defaults.error_warning_send(ctx, text='Kunne ikke finne landet')

            try:
                country_code = data[0]['alpha2Code'].lower()
                capital = data[0]['capital']
                region = data[0]['region']
                sub_region = data[0]['subregion']
                population = data[0]['population']
                population = locale.format_string('%d', population, grouping=True)
                area = int(data[0]['area'])
                area = locale.format_string('%d', area, grouping=True)
                native_name = data[0]['nativeName']
                currency_name = data[0]['currencies'][0]['name']
                currency_abbreviation = data[0]['currencies'][0]['code']
                main_language = data[0]['languages'][0]['name']
                main_language_natvive = data[0]['languages'][0]['nativeName']
                flag = f'https://www.countryflags.io/{country_code}/flat/64.png'
            except TypeError:
                return await Defaults.error_warning_send(ctx, text='Kunne ikke finne landet')

            data_list = [country_code, capital, sub_region, population, area,
                         native_name, currency_name, currency_abbreviation,
                         main_language_natvive, main_language_natvive, flag]

            for i in data_list:
                if not i or i is '':
                    return await Defaults.error_warning_send(ctx, text='Kunne ikke finne landet')

            if main_language != main_language_natvive:
                language = f'{main_language}\n{main_language_natvive}'
            else:
                language = main_language
            
            regions = {
                'Africa': '🌍',
                'Americas': '🌎',
                'Asia': '🌏',
                'Europe': '🌍',
                'Oceania': '🌏' 
            }
            region_globe = regions[region]

            embed = discord.Embed(title=f':flag_{country_code}: {name}', color=ctx.me.color)
            if name != native_name:
                embed.description = f'**{native_name}**\n'
            embed.description += '*Info hentet fra [restcountries.eu](https://restcountries.eu)*'
            embed.set_thumbnail(url=flag)
            embed.add_field(name='📍 Hovedstad', value=capital)
            embed.add_field(name=f'{region_globe} Region', value=sub_region)
            embed.add_field(name='🗣️ Språk', value=language)
            embed.add_field(name='💴 Valuta', value=f'{currency_name}\n{currency_abbreviation}')
            embed.add_field(name='👥 Befolkningstall', value=population)
            embed.add_field(name='📏 Størrelse', value=f'{area} km')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def lmgtfy(self, ctx, *, søkeord: str):
        """Fordi noen trenger en internett 101 leksjon"""

        url = 'https://lmgtfy.com/?' + parse.urlencode({'q': søkeord})

        embed = discord.Embed(color=ctx.me.color, description=f'[Trykk her for løsningen på problemet ditt]({url})')
        embed.set_image(url='http://ecx.images-amazon.com/images/I/51IESUsBdbL._SX258_BO1,204,203,200_.jpg')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def match(self, ctx, *, bruker: discord.Member=None):
        """Se hvor mye du matcher med en annen"""

        if not bruker:
            return await Defaults.error_warning_send(ctx, text='Du må gi meg en bruker')
        if bruker == ctx.author:
            return await Defaults.error_warning_send(ctx, text='Jeg vet du er ensom, men du kan '
                                                               'ikke matche med deg selv')

        async with ctx.channel.typing():

            invoker_id = int(str(ctx.author.id)[11:14])
            user_id = int(str(bruker.id)[11:14])

            match_percent = int((invoker_id + user_id) % 100)

            if bruker.id == self.bot.user.id:
                match_percent = 100
            elif ctx.author.id == 516234701221134346 and bruker.id == 142580278940925953:
                match_percent = 100
            elif ctx.author.id == 142580278940925953 and bruker.id == 516234701221134346:
                match_percent = 100

            await ctx.author.avatar_url_as(format='png').save(
                fp=f'./assets/{ctx.author.id}_raw.png')
            await bruker.avatar_url_as(format='png').save(
                fp=f'./assets/{bruker.id}_raw.png')

            invoker = Image.open(f'./assets/{ctx.author.id}_raw.png').convert('RGBA')
            invoker = invoker.resize((389, 389), Image.ANTIALIAS)
            user = Image.open(f'./assets/{bruker.id}_raw.png').convert('RGBA')
            user = user.resize((389, 389), Image.ANTIALIAS)
            heart = Image.open(f'./assets/heart.png')
            mask = Image.open(f'./assets/heart.png', 'r')

            image = Image.new('RGBA', (1024, 576))
            image.paste(invoker, (0, 94))
            image.paste(user, (635, 94))
            image.paste(heart, (311, 94), mask=mask)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('./assets/fonts/Roboto_Mono/RobotoMono-Medium.ttf', 86)
            font_size = font.getsize(f'{match_percent}%')
            font_size = ((image.size[0] - font_size[0]) / 2, (image.size[1] - font_size[1]) / 2)
            draw.text(font_size, f'{match_percent}%', font=font, fill=(255,255,255,255))

            image.save(f'./assets/{ctx.author.id}_{bruker.id}_edit.png')

            f = discord.File(f'./assets/{ctx.author.id}_{bruker.id}_edit.png')
            embed = discord.Embed()
            embed.set_image(url=f'attachment://{ctx.author.id}_{bruker.id}_edit.png')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed, file=f)

            try:
                remove(f'./assets/{bruker.id}_raw.png')
                remove(f'./assets/{ctx.author.id}_raw.png')
                remove(f'./assets/{ctx.author.id}_{bruker.id}_edit.png')
            except:
                pass


def setup(bot):
    bot.add_cog(Misc(bot))
