from discord.ext import commands


class FunReplies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def react(self, message):
        if message.author.bot:
            return

        if message.content.lower() == 'morn':
            await message.channel.send('Morn')

        elif message.content.lower() == 'no u':
            await message.channel.send(f'no u {message.author.mention}')

        elif message.content.lower() == 'nei du':
            await message.channel.send(f'nei du {message.author.mention}')


def setup(bot):
    bot.add_listener(FunReplies(bot).react, 'on_message')
    bot.add_cog(FunReplies(bot))
