"""
This is a cog made for a specific server
It is not built with any scalability in mind.
This spaghetti code is a quick fix solution built to suit our needs
"""

from discord.ext import commands
import discord

async def emoji_role(emoji):
    emoji = str(emoji)
    roles = {
        '<:tromsogfinnmark:659538517063499776>': 659430999662526464,
        '<:nordland:659524242437832712>': 659431060995702804,
        '<:trondelag:659524239593963561>': 659431100078227486,
        '<:moreogromsdal:659524238868348938>': 659431145280372757,
        '<:innlandet:659524241921933321>': 659431465838444547,
        '<:vestland:659525526418882591>': 659431199936348190,
        '<:viken:659524244157235244>': 659431428223795221,
        '<:oslo:659526028091457550>': 659431468506021889,
        '<:rogaland:659524237706395668>': 659431242281910313,
        '<:vestfoldogtelemark:659524246166306826>': 659431360905084949,
        '<:agder:659524235722752000>': 659431321340477452,
    }
    try:
        role = roles[emoji]
    except:
        return

    return role

class ReactRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = 565230012366848000
        self.channel = 569606841131073546
        self.message = 659563325692313611
        self.emoji = ['<:tromsogfinnmark:659538517063499776>',
                      '<:nordland:659524242437832712>',
                      '<:trondelag:659524239593963561>',
                      '<:moreogromsdal:659524238868348938>',
                      '<:innlandet:659524241921933321>',
                      '<:vestland:659525526418882591>',
                      '<:viken:659524244157235244>',
                      '<:oslo:659526028091457550>',
                      '<:rogaland:659524237706395668>',
                      '<:vestfoldogtelemark:659524246166306826>',
                      '<:agder:659524235722752000>']
    
    async def react_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        if user.bot or payload.message_id != self.message:
            return

        role = await emoji_role(payload.emoji)
        role = guild.get_role(role)
        await user.add_roles(role)
        print('Reacion added')

    async def react_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        if user.bot or payload.message_id != self.message:
            return
        
        role = await emoji_role(payload.emoji)
        role = guild.get_role(role)
        await user.remove_roles(role)
        print('Reacion removed')

    
    @commands.is_owner()
    @commands.command()
    async def addreactions(self, ctx):
        channel = ctx.guild.get_channel(self.channel)
        message = await channel.fetch_message(self.message)
        await ctx.send(':thumbsup:')
        for emoji in self.emoji:
            await message.add_reaction(emoji)


def setup(bot):
    bot.add_listener(ReactRoles(bot).react_add, 'on_raw_reaction_add')
    bot.add_listener(ReactRoles(bot).react_remove, 'on_raw_reaction_remove')
    bot.add_cog(ReactRoles(bot))