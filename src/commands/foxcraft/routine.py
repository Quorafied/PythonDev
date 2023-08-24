from _ownLibrary import *
from database._database import *
from main import function
from imageRecgonition import *
from discord import app_commands
from discord.app_commands import Choice
import discord
from typing import Optional
from discord.ext import commands, tasks


class foxcraftRoutineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.minecraftScript.start()


    @tasks.loop(seconds=15.0)
    async def minecraftScript(self):
        conn = sqlite3.connect("C:/Users/Cosmin/Documents/Code/minecraft/data.db")
        c = conn.cursor()

        c.execute("""SELECT * FROM update_table""")
        rows = c.fetchall()
    
        for listing in rows:
            listing_item, listing_items, listing_price, listing_id = listing[0], listing[1], listing[2], listing[3]
            embed = Embed(color = Color.from_rgb(243, 205, 140))
            embed.set_author(name = "New Listing")

            embed.add_field(name="Item", value = f"x{listing_items} {listing_item}")
            embed.add_field(name="Price", value = f"{listing_price:,.2f}")

            foxDB.c.execute("""DELETE FROM update_table WHERE id=?""", (listing_id,))
            foxDB.commitChanges()
    
        channel = self.bot.get_channel(1131290602902913096)
        if not channel:
            await self.bot.fetch_channel(1131290602902913096).send("hello")

    @commands.Cog.listener()
    async def on_ready(self):
        self.minecraftScript.start()

    @commands.command()
    async def test(self, ctx):
        await ctx.send("test")