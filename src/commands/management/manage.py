from _ownLibrary import *
from main import function
from imageRecgonition import *
class functionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to toggle insult functionality on and off
    @commands.command(name="toggleNo")
    async def toggleNo(self, ctx):
        function.noToggle = not function.noToggle

        if function.noToggle == True:
            if ctx.author.id == ui.ownId:
                ws.toSend_Message = "Toggled on"
                ws.send_response(ui.targetChannelId)

            await ctx.send("Toggled off")

        elif function.noToggle == False:
            if ctx.author.id == ui.ownId:
                ws.toSend_Message = "Toggled off"
                ws.send_response(ui.targetChannelId)

            await ctx.send("Toggled off")