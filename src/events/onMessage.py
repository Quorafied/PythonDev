import discord
from discord.ext import commands
from main import function
from imageRecgonition import *
class onMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """ On_Message event handler """
    @commands.Cog.listener()
    async def on_message(self, message):
        OsuEvent = self.bot.get_cog("osuEvent")
        if message.author.id != function.botId:
            # If a message is not a command, await the following
            if not message.content.startswith(self.bot.command_prefix):
                pass
                # Disabled for now. await OsuEvent.insult(message)
                await OsuEvent.chokeCheck(message)
    