"""
This cog is temporary, due to an influx in bot
accounts joining /r/Norge
"""

from discord.ext import commands

import re
from datetime import datetime


class AntiSelfBot(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 297798952538079233:
            return
        name_match = re.findall(r'[A-Z]+[a-z]+[0-9a-f]{4}', member.name)
        creation_match = (datetime.now() - member.created_at).days
        if name_match != [] and not member.avatar and creation_match < 31:
            role = member.guild.get_role(588432481297104949)
            await member.add_roles(role)

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.command(aliases=['e-nebz', '1nebz'])
    async def enebz(self, ctx):
        if ctx.author.id != 501460926181015554:
            return await ctx.send(f'{ctx.author.mention} er ikke best')
        await ctx.send('Beste karen på serveren 😎')


def setup(bot):
    bot.add_cog(AntiSelfBot(bot))