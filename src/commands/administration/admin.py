from _ownLibrary import *
from main import function
from imageRecgonition import *

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stop")
    @commands.is_owner()
    async def q_stop(self, ctx):
        await self.send_exit_message()
        await self.bot.close()
        exit()

    async def send_exit_message(self):
        Target_Channel_IDs = [ui.botChannelId]
        for channel_id in Target_Channel_IDs:
            target_channel = self.bot.get_channel(channel_id)
            if target_channel:
                await target_channel.send("Quora is taking me offline :(")
        ui.shouldStop = True

        ws.toSend_Message = "Quora is taking me offline :()"
        ws.send_response(ui.targetChannelId)

        ui.stop()

        
