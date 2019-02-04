import discord
import asyncio
from discord.ext import commands

class FunReplies:
    def __init__(self, bot):
        self.bot = bot

    async def react(self, message):
        if message.author.bot:
            return

        if message.content.lower() == "morn":
            await message.channel.send("Morn")

        elif message.content.lower().startswith("no u"):
            await message.channel.send(f"no u {message.author.mention}")

        elif message.content.lower() == "nei du":
            await message.channel.send(f"nei du {message.author.mention}")

def setup(bot):
    n = FunReplies(bot)
    bot.add_listener(n.react, "on_message")
    bot.add_cog(n)