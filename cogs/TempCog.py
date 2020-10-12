"""
This is a cog made for a specific server
It is not built with any scalability in mind.
This spaghetti code is a quick fix solution built to suit our needs
"""

from discord.ext import commands

import re


class TempCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.channel.id != 696776618525589574 or message.author.bot:
            return

        pattern = r'[S|s]piller:\s\w+\n[M|m]ap:\shttps:\/\/osu\.ppy\.sh\/beatmapsets\/\d+#\w+\/\d+'
        if re.search(pattern, message.clean_content):
            await message.add_reaction('👍')
            await message.add_reaction('👎')


def setup(bot):
    bot.add_listener(TempCog(bot).on_message, 'on_message')
    bot.add_cog(TempCog(bot))
