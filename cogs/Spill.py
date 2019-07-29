from discord.ext import commands
import discord

import asyncio
import time
import random

from cogs.utils import Defaults


class Spill(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.group(aliases=['typingtest', 'typing', 'skrive'])
    async def skrivetest(self, ctx):
        """Sjekk hvor fort du skriver"""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            self.bot.get_command(f'{ctx.command}').reset_cooldown(ctx)

    @commands.cooldown(1, 60, commands.BucketType.guild)
    @skrivetest.command(aliases=['top200', 'top', 'topp'])
    async def topp200(self, ctx, *, språk: str):
        """Skrivetest for topp 200 ord i et valgt språk"""

        languages = {
            'engelsk': 'english_top200',
            'norsk': 'norwegian_top200',
            'tysk': 'german_top200'
        }
        available_languages = []
        try:
            path = languages[språk]
        except KeyError:
            for key, value in languages.items():
                available_languages.append(key)
            available_languages = ', '.join(available_languages)
            self.bot.get_command('skrivetest topp200').reset_cooldown(ctx)
            return await Defaults.error_warning_send(ctx, text=f'Du må velge et språk fra listen\n```{available_languages}```')

        random_num = random.randint(30, 70)
        with open(f'./assets/{path}_words.txt', 'r', encoding='utf-8') as f:
            words = [line.split(',') for line in f.readlines()]
            words = words[0]
            random.shuffle(words)
            text = ' '.join(words[:random_num])

        length_chars = len(text)
        length_words = len(text.split(' '))

        timeout = float(int(1.714 * length_words))

        if str(ctx.author.color) != '#000000':
            color = ctx.author.color
        else:
            color = discord.Colour(0x99AAB5)

        embed = discord.Embed(color=color, description=f'Testen starter når en tekst kommer opp og ender når du har sendt meldingen. Du har `{int(timeout)}` sekunder på deg\n\nTesten starter om 5 sekunder...')
        await Defaults.set_footer(ctx, embed)
        await ctx.send(embed=embed)

        await asyncio.sleep(5)

        embed = discord.Embed(color=color, description=f'**{text}**')
        await Defaults.set_footer(ctx, embed)
        status_msg = await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.message.channel
        
        try:
            msg = await self.bot.wait_for('message', timeout=timeout, check=check)
        except asyncio.TimeoutError:
            return await Defaults.error_fatal_edit(ctx, status_msg, text='Du svarte ikke i tide!', mention=False)
        else:
            counter = int((msg.created_at - status_msg.created_at).total_seconds())
            minutes = counter / 60
            cpm = round(length_chars / minutes)
            wpm = round(length_words / minutes)

            if wpm > 200:
                self.bot.get_command(f'{ctx.command}').reset_cooldown(ctx)
                return await Defaults.error_warning_send(ctx, text='Eh... Tror ærlig ikke at du skriver så fort asså 😄')

            index = 0
            wrong_words = 0
            text = text.split(' ')
            answer = msg.clean_content.split(' ')
            for word in text:
                try:
                    if word != answer[index]:
                        wrong_words += 1
                except IndexError:
                    wrong_words += 1
                index += 1

            embed = discord.Embed(color=color, title='Resultat',
            description=f'**WPM:** `{wpm}`\n**CPM:** `{cpm}`\n**Tid:** `{counter}` sekunder\n**Lengde:** `{length_words}` ord (`{length_chars}` tegn)\n**Feil:** `{wrong_words}`')
            await Defaults.set_footer(ctx, embed)
            await ctx.send(embed=embed)

            self.bot.get_command(f'{ctx.command}').reset_cooldown(ctx)


def setup(bot):
    bot.add_cog(Spill(bot))

    