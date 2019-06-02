import discord
from discord.ext import commands

from codecs import open
from json import load as json_load

from requests import get
from random import randint, choice
from hashlib import md5
from bs4 import BeautifulSoup
from datetime import datetime
from re import sub, split

from .utils import Defaults

with open('config.json', 'r', encoding='utf8') as f:
    config = json_load(f)
    prefix = config['prefix']


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
            return await ctx.send(embed=embed)

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
            return await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def drepmeg(self, ctx):
        """Dreper deg"""

        await ctx.send("Du er død nå")

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
            embed.add_field(
            name='Kukstørrelse', value=f'18.1 cm lang\n16.5 cm girth')
        else:
            embed.add_field(
                name='Kukstørrelse', value=f'{dick_size} cm\n8{dick_drawing}D')
        
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command()
    async def roll(self, ctx):
        """Gir deg et tilfeldig tall"""

        await ctx.send(str(randint(0, 100)))

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(name='8ball')
    async def ball8(self, ctx, *, spørsmål):
        """Svarer på dine dypeste spørsmål"""

        if spørsmål[-1:] != '?':
            return await Defaults.error_warning_send(
                ctx, text='Du må stille meg et spørsmål da dømdøm!',
                mention=False)

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

        await ctx.send(choice(answers))

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

        tekst = sub("'|,", "", str(tekst))
        tekst = sub('r|l', 'w', tekst)
        tekst = sub('R|L', 'W', tekst)
        tekst = sub('n', 'ny', tekst)
        tekst = sub('N', 'Ny', tekst)
        tekst = sub('ove', 'uv', tekst)
        # tekst = sub('!', ' (・`ω´・)', tekst) https://kaomoji.moe/

        if not tekst or len(tekst) >= 1000:
            return await Defaults.error_warning_send(
                ctx, text='Teksten er for lang', mention=False)

        embed = discord.Embed(color=ctx.me.color, description=tekst)
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['urban', 'dictionary', 'ordbok'])
    async def urbandictionary(self, ctx, *ord):
        """Sjekk definisjonen av et ord"""

        async with ctx.channel.typing():

            try:
                data = get('https://api.urbandictionary.com/' +
                           f'v0/define?term={ord}').json()
                urban_url = data['list'][0]['permalink']
            except IndexError:
                return await Defaults.error_fatal_send(
                    ctx,
                    text='Fant ingen definisjon for dette ordet!',
                    mention=False)

            word = data['list'][0]['word']
            submitter = data['list'][0]['author']
            definition = sub(';|\[|\]', '', data['list'][0]['definition'])
            example = sub(';|\[|\]', '', data['list'][0]['example'])
            upvotes = data['list'][0]['thumbs_up']
            downvotes = data['list'][0]['thumbs_down']

            embed = discord.Embed(
                title=word, color=ctx.me.color,
                url=urban_url, description=f'**Definert av:** {submitter}')
            embed.set_author(
                name='Urban Dictionary',
                icon_url='https://a2.mzstatic.com/us/r30/Purple/v4/dd/ef/75/' +
                         'ddef75c7-d26c-ce82-4e3c-9b07ff0871a5/' +
                         'mzl.yvlduoxl.png')
            embed.add_field(name='Definisjon', value=definition)
            embed.add_field(name='Eksempel', value=example, inline=False)
            embed.add_field(
                name='Vurdering',
                value=f':thumbsup: {upvotes} / :thumbsdown: {downvotes}',
                inline=False)
            await Defaults.set_footer(ctx, embed)
            return await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=['isitdown', 'checksite'])
    async def isitup(self, ctx, nettside: str):
        """Sjekk om en nettside er oppe"""

        async with ctx.channel.typing():

            data = get(f'https://isitup.org/{nettside}')
            scraped = BeautifulSoup(data.text, 'html.parser')
            status = scraped.find('p').get_text()
            nettside = scraped.find(class_='domain').get_text()
            website_url = scraped.find(class_='domain')['href']

            embed = discord.Embed(
                title=nettside.capitalize(),
                url=website_url, timestamp=datetime.utcnow())

            if status[-6:] == 'is up.':
                status = 'Oppe!'
                ping = scraped.find(class_='smaller').get_text()
                pinglist = []
                for i in ping.split():
                    if i.isdigit():
                        pinglist.append(i)
                embed.add_field(name='Ping', value=f'{pinglist[0]} ms')
                embed.color = 0x2ECC71
            else:
                status = 'Nede!'
                embed.color = 0xff0000

            embed.add_field(name='Status', value=status)
            return await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['clapify'])
    async def klappifiser(self, ctx, *, tekst):
        """Klapppifiserer teksten din"""

        if not tekst or len(tekst) >= 1000:
            return await Defaults.error_warning_send(
                ctx, text='Teksten er for lang', mention=False)

        tekst = sub(' ', '👏', tekst)

        embed = discord.Embed(
            color=ctx.me.color, description=f'**{tekst.upper()}**')
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
                return await Defaults.error_warning_send(
                    ctx, text='Du er ikke koblet til en talekanal',
                    mention=False)

            link = 'https://canary.discordapp.com/channels/' +\
                   f'{ctx.guild.id}/{voice_channel_id}'
            embed = discord.Embed(
                title=f'Videochat: {ctx.author.voice.channel.name}',
                color=ctx.me.color,
                description=f'[Trykk her for å bli med i videochat]({link})')
            return await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['timezone', 'tid', 'tidssone', 'klokken'])
    async def klokka(self, ctx, kontinent, by):
        """Se hvor mye klokka er i et bestemt område"""

        async with ctx.channel.typing():

            try:
                data = get(
                    'http://worldtimeapi.org/api/timezone/' +
                    f'{kontinent.capitalize()}/{by.capitalize()}').json()
                timezone = data['timezone']
            except KeyError:
                return await Defaults.error_warning_send(
                    ctx,
                    text='Kunne ikke finne sted/tidssone',
                    mention=False)

            timezone = split('/', timezone)
            timezone_local = data['abbreviation']
            timezone_utc = data['utc_offset']
            time_norway = datetime.now().strftime('%H:%M\n%d.%m.%Y')

            time = data['datetime']
            time_formatted = f'{time[11:16]}\n{time[8:10]}.' +\
                             f'{time[5:7]}.{time[:4]}'

            daylight_savings = data['dst']
            if daylight_savings is False:
                daylight_savings = 'Nei'
            else:
                daylight_savings = 'Ja'

            embed = discord.Embed(
                title=f'Klokka i {timezone[1]}',
                color=0x0085ff, timestamp=datetime.utcnow())
            embed.add_field(name='Klokka', value=time_formatted)
            embed.add_field(name='Klokka i Norge', value=time_norway)
            embed.add_field(name='Sommertid', value=daylight_savings)
            embed.add_field(name='UTC tidssone', value=timezone_utc)
            embed.add_field(
                name='Standard tidssone for sted', value=timezone_local)
            embed.set_footer(text='Klokka i din tidssone ->')

            return await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['country'])
    async def land(self, ctx, *, land: str):
        """Se info om et land"""

        async with ctx.channel.typing():

            try:
                data = get(
                    f'https://restcountries.eu/rest/v2/name/{land}').json()
                name = data[0]['name']
            except KeyError:
                return await Defaults.error_warning_send(
                    ctx,
                    text='Kunne ikke finne landet',
                    mention=False)

            try:
                country_code = data[0]['alpha2Code'].lower()
                capital = data[0]['capital']
                sub_region = data[0]['subregion']
                population = data[0]['population']
                area = int(data[0]['area'])
                native_name = data[0]['nativeName']
                currency_name = data[0]['currencies'][0]['name']
                currency_abbreviation = data[0]['currencies'][0]['code']
                main_language = data[0]['languages'][0]['name']
                main_language_natvive = data[0]['languages'][0]['nativeName']
                flag = 'https://www.countryflags.io/' +\
                       f'{country_code}/flat/64.png'
            except TypeError:
                return await Defaults.error_warning_send(
                    ctx, text='Kunne ikke finne landet', mention=False)

            data_list = [country_code, capital, sub_region, population, area,
                         native_name, currency_name, currency_abbreviation,
                         main_language_natvive, main_language_natvive, flag]

            for i in data_list:
                if not i or i is '':
                    return await Defaults.error_warning_send(
                        ctx, text='Kunne ikke finne landet', mention=False)

            if main_language != main_language_natvive:
                language = f'{main_language}\n{main_language_natvive}'
            else:
                language = main_language

            embed = discord.Embed(
                title=f':flag_{country_code}: {name}',
                color=ctx.me.color, timestamp=datetime.utcnow())
            if name == native_name:
                embed.description = native_name
            embed.set_thumbnail(url=flag)
            embed.add_field(name='Hovedstad', value=capital)
            embed.add_field(name='Region', value=sub_region)
            embed.add_field(name='Språk', value=language)
            embed.add_field(name='Valuta',
                            value=f'{currency_name}\n{currency_abbreviation}')
            embed.add_field(
                name='Befolkningstall', value=population)
            embed.add_field(
                name='Størrelse', value=f'{area}km')

            return await ctx.send(embed=embed)

    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def lmgtfy(self, ctx, mention: discord.Member=None, *, søkeord: str):
        """Fordi noen trenger en internett 101 leksjon"""

        embed = discord.Embed(
            color=ctx.me.color,
            description='[Trykk her for løsningen ' +
            f'på problemet ditt](https://lmgtfy.com/?q={søkeord})')
        embed.set_image(
            url='http://ecx.images-amazon.com/images/I/' +
                '51IESUsBdbL._SX258_BO1,204,203,200_.jpg')
        embed.set_footer(
            text=f'{mention.name}#{mention.discriminator}',
            icon_url=mention.avatar_url)
        if not mention:
            return await ctx.send(embed=embed)
        await ctx.send(embed=embed, content=mention.mention)


def setup(bot):
    bot.add_cog(Misc(bot))
