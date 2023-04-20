# Import required dependencies
from _ownLibrary import *
from imageRecgonition import *
from discord import app_commands
import threading
# Initialize the Bot with the command prefix



# *----------------------------------------------*
# |                  Bot setup                   |
# *----------------------------------------------*

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

client = commands.Bot(command_prefix='q.', intents=intents)
# *----------------------------------------------*

loop = asyncio.get_event_loop()


# *----------------------------------------------*
# |                  Function                    |
# *----------------------------------------------*

class functions():
    def __init__(self):
        self.noToggle = False
        self.running = False
        self.uptime = 0
        self.startTime = time.time()
        self.canInsult = True
        client.remove_command("help")

        self.botId = 861370829253509133

        self.getUser_String = ""
        self.status_String = ""

    def onStart(self):
        self.running = True
        self.noToggle = False
        self.startTime = time.time()

    def show_upTime(self):
        elapsed_time = time.time() - self.startTime

        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{int(hours)}h{int(minutes)}m{int(seconds)}s "

    def showStatus(self):
        
        embed = Embed(
            title="Status for Quora Env Bot",
            description="Help command: `q.help`",
            color=Color.from_rgb(243, 205, 140)
        )

        embed.add_field(name="Uptime:", value=self.show_upTime(), inline=True)

        embed.add_field(name=" ", value=" ", inline=False)

        embed.add_field(name="Can insult:", value=f"> {function.canInsult}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Can no:", value=f"> {function.noToggle}", inline=True)
                                # Title            Description                 Uptime                     Uptime Value                  Can Insult                       Can no                    Can Insult Value                 Can No value       
        ws.toSend_Message = f"**{embed.title}**\n{embed.description}\n\n**{embed.fields[0].name}**\n{embed.fields[0].value}\n\n**{embed.fields[2].name}**        **{embed.fields[4].name}**\n{embed.fields[2].value[2:]}                     {embed.fields[4].value[2:]}"
        return embed
    
function = functions()
# *----------------------------------------------*



# *----------------------------------------------*
# |                  on_ready                    |
# *----------------------------------------------*

async def send_start_message():
    Target_Channel_IDs = [ui.targetChannelId, ui.botChannelId]
    for channel_id in Target_Channel_IDs:
        target_channel = client.get_channel(channel_id)
        if target_channel:
            await target_channel.send("Quora revived me! :D")

    ws.toSend_Message = "Quora revived me! :D"
    ws.send_response(ui.targetChannelId)
    time.sleep(1)
    ui.running = True

# Event handler for when the bot is ready to be used
@client.event
async def on_ready():
    function.onStart()
    await send_start_message()

    print("Ready to attack!")
    # Change bot nickname in the first guild it's connected to
    #await client.guilds[0].me.edit(nick="Depressed Bot", )    
# *----------------------------------------------*


from commands.osu.osu_commands import *
from commands.information.informations import *
from commands.administration.admin import *
from commands.management.manage import *
from events.onMessage import *
from events.osu_events import *

async def load():
    await client.add_cog(informations(client))
    await client.add_cog(osuCommands(client))   
    await client.add_cog(Admin(client))
    await client.add_cog(functionManager(client))

    await client.add_cog(onMsg(client))
    
    await client.add_cog(osuEvent(client))



async def main():
    await load()
    await client.start(botToken)



async def run_in_thread():
    await asyncio.to_thread(doit)

def doit():            
    while True:
        if ui.running == False:
            print("Bot has not started yet..\n\n\n")
            pass
        else:
            message = ui.check_forNewMessage()
            if message is False:
                pass
            else:
                ui.send_messageToBot(message)
        time.sleep(1)
        


async def mainHandler():
    print("Starting gather")    
    await asyncio.gather(
        run_in_thread(),
        main()
    )

if __name__ == "__main__":
    time.sleep(2)
    loop.run_until_complete(mainHandler())
#client.run(botToken, reconnect=True)