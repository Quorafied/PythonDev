from _ownLibrary import *
from imageRecgonition import *
from discord import *
from discord.app_commands import CommandTree
from apikeys import *
from database._database import *

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.emojis_and_stickers = True
intents.reactions = True

# discord.Permissions.read_message_history

from commands.foxcraft.foxcraft import *
from commands.osu.osu_commands import *
from commands.information.informations import *
from commands.administration.admin import *
from commands.management.manage import *
from events.onMessage import *
from events.osu_events import *
from commands.foxcraft.routine import *

class SlashBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='q.', intents=intents)

    async def setup_hook(self):
        self.remove_command("help")
        await self.add_cog(foxcraftSlashCog(self))
        await self.add_cog(foxcraftCog(self))
        await self.add_cog(osuCommands(self))
        await self.add_cog(informations(self))
        await self.add_cog(Admin(self))
        await self.add_cog(functionManager(self))
        await self.add_cog(onMsg(self))
        await self.add_cog(osuEvent(self))
        # await self.add_cog(foxcraftRoutineCog(self))
        self.tree.copy_global_to(guild=discord.Object(id=584405834843291649))
        await self.tree.sync()

bot = SlashBot()        

@bot.event
async def on_ready():
    # await minecraftScript()
    print("Ready!")

bot.run(botToken)





