from _ownLibrary import *
from main import function
from imageRecgonition import *

class informations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command(name="status")
    async def showStatus(self, ctx):
        await ctx.send(embed = function.showStatus())

        print("send status back \n")
        # WS Message is loaded in function.showStatus()
        ws.send_response(ui.targetChannelId)
        print(ws.toSend_Message)

    @commands.command(name="help")
    async def showHelp(self, ctx):
        embed = Embed(
            title="Help information",
            description="Currently available commands: **status, help, toggleNo, getUser**",
            color=Color.from_rgb(243, 205, 140)
        )

        ws.toSend_Message = f"**{embed.title}**\n\n{embed.description}"
        ws.send_response(ui.targetChannelId)
        await ctx.send(embed=embed)
