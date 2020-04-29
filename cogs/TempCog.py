"""
This is a cog made for a specific server
It is not built with any scalability in mind.
This spaghetti code is a quick fix solution built to suit our needs
"""

from discord.ext import commands
import discord


class TempCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message):
        if message.channel.id != 696776618525589574 or message.author.bot:
            return
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    @commands.command(name='4wc')
    async def _4wc(self, ctx):

        if ctx.channel.id == 569615483184349193:
            role_4wc = ctx.guild.get_role(704962348502482984)
            await ctx.author.add_roles(role_4wc)
            await ctx.send('👍', delete_after=5.0)
            await ctx.message.delete()


def setup(bot):
    bot.add_listener(TempCog(bot).on_message, 'on_message')
    bot.add_cog(TempCog(bot))